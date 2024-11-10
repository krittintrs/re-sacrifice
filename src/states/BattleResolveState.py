import random
from src.states.BaseState import BaseState
from src.dependency import *
from src.constants import *
from src.Render import *
from src.battleSystem.Buff import Buff
import pygame
import sys
import math

class BattleResolveState(BaseState):
    def __init__(self):
        super(BattleResolveState, self).__init__()

    def Enter(self, params):
        print("\n>>>>>> Enter BattleResolveState <<<<<<")
        self.player = params['player']
        self.enemy = params['enemy']
        self.field = params['field']
        self.turn = params['turn']
        self.currentTurnOwner = params['currentTurnOwner']
        self.effectOrder = params['effectOrder']

        # apply buff to all cards on hand
        self.player.apply_buffs_to_cardsOnHand()
        self.enemy.apply_buffs_to_cardsOnHand()

        # display entity stats
        self.player.display_stats()
        self.enemy.display_stats()

    def Exit(self):
        pass

    def update(self, dt, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_SPACE:
                    pass
                if event.key == pygame.K_RETURN:
                    pass
            
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
                g_state_manager.Change(BattleState.END_PHASE, {
                    'player': self.player,
                    'enemy': self.enemy,
                    'field': self.field,
                    'turn': self.turn,
                    'currentTurnOwner': self.currentTurnOwner
                })
            else:
                if self.player.health <= 0:
                    self.winner = PlayerType.ENEMY
                elif self.enemy.health <= 0:
                    self.winner = PlayerType.PLAYER
                g_state_manager.Change(BattleState.FINISH_PHASE, {
                    'player': self.player,
                    'enemy': self.enemy,
                    'field': self.field,
                    'turn': self.turn,
                    'currentTurnOwner': self.currentTurnOwner,
                    'winner': self.winner
                })
            
        for buff in self.player.buffs:
            buff.update(dt, events)
        for buff in self.enemy.buffs:
            buff.update(dt, events)

        self.player.update(dt)
        self.enemy.update(dt)
        
    def resolveCardEffect(self, effect, effectOwner):
        if not ((effectOwner == PlayerType.PLAYER and self.player.stunt == True) or (effectOwner == PlayerType.ENEMY and self.enemy.stunt == True)):
           match effect.type:
                case EffectType.ATTACK | EffectType.ATTACK_SELF_BUFF | EffectType.ATTACK_OPPO_BUFF:
                    g_state_manager.Change(SelectionState.ATTACK, {
                        'player': self.player,
                        'enemy': self.enemy,
                        'field': self.field,
                        'turn': self.turn,
                        'currentTurnOwner': self.currentTurnOwner,
                        'effectOrder': self.effectOrder,
                        'effect': effect,
                        'effectOwner': effectOwner
                    })
                case EffectType.MOVE:
                    g_state_manager.Change(SelectionState.MOVE, {
                        'player': self.player,
                        'enemy': self.enemy,
                        'field': self.field,
                        'turn': self.turn,
                        'currentTurnOwner': self.currentTurnOwner,
                        'effectOrder': self.effectOrder,
                        'effect': effect,
                        'effectOwner': effectOwner
                    })
                case EffectType.OPPO_BUFF:
                    g_state_manager.Change(SelectionState.BUFF, {
                        'player': self.player,
                        'enemy': self.enemy,
                        'field': self.field,
                        'turn': self.turn,
                        'currentTurnOwner': self.currentTurnOwner,
                        'effectOrder': self.effectOrder,
                        'effect': effect,
                        'effectOwner': effectOwner
                    })
                case EffectType.SELF_BUFF:
                    buffList = self.getBuffListFromEffect(effect)
                    print(f'{effectOwner.name} self buff: {buffList}')
                    if effectOwner == PlayerType.PLAYER:
                        self.player.add_buffs(buffList)
                    elif effectOwner == PlayerType.ENEMY:
                        self.enemy.add_buffs(buffList)
                case EffectType.PUSH:
                    g_state_manager.Change(SelectionState.PUSH, {
                        'player': self.player,
                        'enemy': self.enemy,
                        'field': self.field,
                        'turn': self.turn,
                        'currentTurnOwner': self.currentTurnOwner,
                        'effectOrder': self.effectOrder,
                        'effect': effect,
                        'effectOwner': effectOwner
                    })
                case EffectType.PULL:
                    g_state_manager.Change(SelectionState.PULL, {
                        'player': self.player,
                        'enemy': self.enemy,
                        'field': self.field,
                        'turn': self.turn,
                        'currentTurnOwner': self.currentTurnOwner,
                        'effectOrder': self.effectOrder,
                        'effect': effect,
                        'effectOwner': effectOwner
                    })
                case EffectType.CLEANSE:
                    if effectOwner == PlayerType.PLAYER:
                        for buff in self.player.buffs:
                            if buff.type == BuffType.DEBUFF:
                                buff.duration = 0
                        self.player.remove_expired_buffs()
                    elif effectOwner == PlayerType.ENEMY:
                        for buff in self.enemy.buffs:
                            if buff.type == BuffType.DEBUFF:
                                buff.duration = 0
                        self.enemy.remove_expired_buffs()
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
                        g_state_manager.Change(SelectionState.MOVE, {
                        'player': self.player,
                        'enemy': self.enemy,
                        'field': self.field,
                        'turn': self.turn,
                        'currentTurnOwner': self.currentTurnOwner,
                        'effectOrder': self.effectOrder,
                        'effect': effect,
                        'effectOwner': effectOwner
                    })
                case EffectType.BLOOD_SACRIFICE:
                    hp_paid = math.floor(self.player.health * 0.3)
                    self.player.health -= hp_paid
                    buffList = self.getBuffListFromEffect(effect)
                    buffList[0].value[0] = hp_paid
                    self.player.add_buffs(buffList)
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
                        self.player.add_buffs([critical_buff])
                # MAGE CLASS
                case EffectType.TRUE_DAMAGE:
                    pass
                case EffectType.NEXT_MULTI:
                    pass
                # BOSSES
                case EffectType.KAMIKAZE:
                    pass
                case EffectType.SPAWN:
                    pass
                case EffectType.HEAL:
                    pass
                case EffectType.COPY:
                    pass
                case _:
                    print(f'Unknown effect type: {effect.type}')
        else:
            print('stunt')
            g_state_manager.Change(BattleState.RESOLVE_PHASE, {
                            'player': self.player,
                            'enemy': self.enemy,
                            'field': self.field,
                            'turn': self.turn,
                            'currentTurnOwner': self.currentTurnOwner,
                            'effectOrder': self.effectOrder
                        })

    def getBuffListFromEffect(self, effect):
        buffList = []
        if effect.buffNameList:
            for buffName in effect.buffNameList:
                buffList.append(Buff(CARD_BUFF[buffName])) 
            return buffList
        else:
            print(f'Buff not found: {effect.buffNameList}')
            return False

    def render(self, screen):
        RenderTurn(screen, 'Resolve State', self.turn, self.currentTurnOwner)
        RenderEntityStats(screen, self.player, self.enemy)
        RenderSelectedCard(screen, self.player.selectedCard, self.enemy.selectedCard)

        # Render field
        for fieldTile in self.field:
            fieldTile.render(screen)
