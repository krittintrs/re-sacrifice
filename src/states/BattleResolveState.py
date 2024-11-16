import random
from src.states.BaseState import BaseState
from src.dependency import *
from src.constants import *
from src.Pause import *
from src.Render import *
from src.battleSystem.Buff import Buff
import pygame
import sys
import math

class BattleResolveState(BaseState):
    def __init__(self):
        super(BattleResolveState, self).__init__()
        self.pauseHandler = PauseHandler()

    def Enter(self, params):
        print("\n>>>>>> Enter BattleResolveState <<<<<<")
        # print(params)
        self.params = params
        battle_param = self.params['battleSystem']
        self.player = battle_param['player']
        self.enemy = battle_param['enemy']
        self.field = battle_param['field']
        self.turn = battle_param['turn']
        self.currentTurnOwner = battle_param['currentTurnOwner']
        self.effectOrder = battle_param['effectOrder']

        # apply buff to all cards on hand
        self.player.apply_buffs_to_cardsOnHand()
        self.enemy.apply_buffs_to_cardsOnHand()

        # display entity stats
        self.player.display_stats()
        self.enemy.display_stats()

    def Exit(self):
        pass

    def remove_timeout_entity(self):
        for tile in self.field:
            if tile.is_second_entity():
                if tile.second_entity.duration == 0:
                    print("remove second entity for timeout ", tile.index)
                    tile.remove_second_entity()

    def update(self, dt, events):
        if self.pauseHandler.is_paused():
            self.pauseHandler.update(dt, events, self.params)
            return
        
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.pauseHandler.pause_game()
            
        if self.effectOrder["before"]:
            print(self.effectOrder["before"][0][0].type)
            effect = self.effectOrder["before"].pop(0)
            self.resolveCardEffect(effect[0], effect[1])
        elif self.effectOrder["main"]:
            print(self.effectOrder["main"][0][0].type)
            effect = self.effectOrder["main"].pop(0)
            self.resolveCardEffect(effect[0], effect[1])
        elif self.effectOrder["after"]:
            print(self.effectOrder["after"][0][0].type)
            effect = self.effectOrder["after"].pop(0)
            self.resolveCardEffect(effect[0], effect[1])
        else:
            if self.player.health > 0 and self.enemy.health > 0:
                self.params['battleSystem'] = {
                    'player': self.player,
                    'enemy': self.enemy,
                    'field': self.field,
                    'turn': self.turn,
                    'currentTurnOwner': self.currentTurnOwner
                }
                g_state_manager.Change(BattleState.END_PHASE, self.params)
            else:
                if self.player.health <= 0:
                    self.winner = PlayerType.ENEMY
                elif self.enemy.health <= 0:
                    self.winner = PlayerType.PLAYER
                self.params['battleSystem'] = {
                    'player': self.player,
                    'enemy': self.enemy,
                    'field': self.field,
                    'turn': self.turn,
                    'currentTurnOwner': self.currentTurnOwner,
                    'winner': self.winner
                }
                g_state_manager.Change(BattleState.FINISH_PHASE, self.params)
            
        for buff in self.player.buffs:
            buff.update(dt, events)
        for buff in self.enemy.buffs:
            buff.update(dt, events)

        self.player.update(dt)
        self.enemy.update(dt)

        for tile in self.field:
            if tile.second_entity:
                tile.second_entity.update(dt)
            elif tile.is_occupied() and tile.entity.type == None:
                tile.entity.update(dt)

        self.remove_timeout_entity()
        
    def resolveCardEffect(self, effect, effectOwner):
        if not ((effectOwner == PlayerType.PLAYER and self.player.stunt == True) or (effectOwner == PlayerType.ENEMY and self.enemy.stunt == True)):
            self.params['battleSystem'] = {
                'player': self.player,
                'enemy': self.enemy,
                'field': self.field,
                'turn': self.turn,
                'currentTurnOwner': self.currentTurnOwner,
                'effectOrder': self.effectOrder,
                'effect': effect,
                'effectOwner': effectOwner
            }
            match effect.type:
                case EffectType.ATTACK | EffectType.ATTACK_SELF_BUFF | EffectType.ATTACK_OPPO_BUFF | EffectType.TRUE_DAMAGE:
                    g_state_manager.Change(SelectionState.ATTACK, self.params)
                case EffectType.MOVE:
                    g_state_manager.Change(SelectionState.MOVE, self.params)
                case EffectType.OPPO_BUFF:
                    g_state_manager.Change(SelectionState.BUFF, self.params)
                case EffectType.SELF_BUFF:
                    buff = self.getBuffFromEffect(effect)
                    print(f'{effectOwner.name} self buff: {buff}')
                    if effectOwner == PlayerType.PLAYER:
                        self.player.ChangeAnimation("cast_loop")
                        self.player.add_buff(buff)
                    elif effectOwner == PlayerType.ENEMY:
                        self.enemy.add_buff(buff)
                case EffectType.PUSH:
                    g_state_manager.Change(SelectionState.PUSH, self.params)
                case EffectType.PULL:
                    g_state_manager.Change(SelectionState.PULL, self.params)
                case EffectType.CLEANSE:
                    if effectOwner == PlayerType.PLAYER:
                        for buff in self.player.buffs:
                            if buff.type == BuffType.DEBUFF:
                                buff.duration = 0
                        self.player.remove_expired_buffs()
                        self.player.vfx.play("buff_vfx")
                    elif effectOwner == PlayerType.ENEMY:
                        for buff in self.enemy.buffs:
                            if buff.type == BuffType.DEBUFF:
                                buff.duration = 0
                        self.enemy.remove_expired_buffs()
                        self.enemy.vfx.play("buff_vfx")
                case EffectType.DISCARD:
                    pass
                case EffectType.SAND_THROW:
                    pass
                case EffectType.ANGEL_BLESSING:
                    pass
                case EffectType.DESTINY_DRAW:
                    pass
                case EffectType.RESET_HAND:
                    pass
                # WARRIOR CLASS
                case EffectType.WARRIOR:
                    if len(self.player.buffs) >= 1 and self.player.job == PlayerClass.WARRIOR:
                        g_state_manager.Change(SelectionState.MOVE, self.params)
                case EffectType.BLOOD_SACRIFICE:
                    hp_paid = math.floor(self.player.health * 0.3)
                    self.player.health -= hp_paid
                    buff = self.getBuffFromEffect(effect)
                    buff.value[0] = hp_paid
                    self.player.ChangeAnimation("cast")
                    self.player.add_buff(buff)
                # RANGER CLASS
                case EffectType.CRITICAL:
                    chance = random.randint(1, 6)
                    threshold = 2
                    for buff in self.player.buffs:
                        if buff.type == BuffType.CRIT_RATE:
                            threshold = 4
                            break
                    print(f'{chance} <= {threshold}')
                    if chance <= threshold:
                        print('Critical hit!')
                        critical_buff = Buff(CARD_BUFF['critical_buff'])
                        critical_buff.value[0] = self.player.selectedCard.attack // 2
                        self.player.ChangeAnimation("cast")
                        self.player.add_buff(critical_buff)
                # MAGE CLASS
                case EffectType.NEXT_MULTI:
                    pass
                # BOSSES
                case EffectType.KAMIKAZE:
                    pass
                case EffectType.SPAWN:
                    g_state_manager.Change(SelectionState.SPAWN, self.params)
                case EffectType.HEAL:
                    if effectOwner == PlayerType.ENEMY:
                        self.enemy.health += self.enemy.maxhealth // 2
                        self.enemy.vfx.play("heal_vfx")
                        if self.enemy.health > self.enemy.maxhealth:
                            self.enemy.health = self.enemy.maxhealth
                case EffectType.COPY:
                    pass
                case _:
                    print(f'Unknown effect type: {effect.type}')
        else:
            print('stunt')
            self.params['battleSystem'] = {
                'player': self.player,
                'enemy': self.enemy,
                'field': self.field,
                'turn': self.turn,
                'currentTurnOwner': self.currentTurnOwner,
                'effectOrder': self.effectOrder
            }
            g_state_manager.Change(BattleState.RESOLVE_PHASE, self.params)

    def getBuffFromEffect(self, effect):
        if effect.buffName:
            buff = Buff(CARD_BUFF[effect.buffName])
            return buff
        else:
            print(f'Buff not found: {effect.buffName}')
            return False

    def render(self, screen):
        RenderTurn(screen, "battleResolve", self.turn, self.currentTurnOwner)
        RenderEntityStats(screen, self.player, self.enemy)
        RenderSelectedCard(screen, self.player.selectedCard, self.enemy.selectedCard)

        # Render field
        for fieldTile in self.field:
            fieldTile.render(screen)

        self.pauseHandler.render(screen)
