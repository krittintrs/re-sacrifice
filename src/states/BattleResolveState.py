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
        self.land_hit = params['land_hit'] # keep track whether enemy of player land a hit ["player":False,"enemy":False]

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
            for effectDetail in self.effectOrder["before"]:
                print(effectDetail[0].type)
                self.resolveCardEffect(effectDetail[0], effectDetail[1])
                self.effectOrder["before"].remove(effectDetail)
        elif self.effectOrder["main"]:
            for effectDetail in self.effectOrder["main"]:
                self.resolveCardEffect(effectDetail[0], effectDetail[1])
                self.effectOrder["main"].remove(effectDetail)
        elif self.effectOrder["after"]:
            for effectDetail in self.effectOrder["after"]:
                self.resolveCardEffect(effectDetail[0], effectDetail[1])
                self.effectOrder["after"].remove(effectDetail)
        else:
            if self.player.health > 0 and self.enemy.health > 0:
                g_state_manager.Change(BattleState.END_PHASE, {
                    'player': self.player,
                    'enemy': self.enemy,
                    'field': self.field,
                    'turn': self.turn,
                    'currentTurnOwner': self.currentTurnOwner,
                    'land_hit':self.land_hit
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

    def resolveCardEffect(self, effect, effectOwner):
        match effect.type:
            case EffectType.ATTACK:
                g_state_manager.Change(SelectionState.ATTACK, {
                    'player': self.player,
                    'enemy': self.enemy,
                    'field': self.field,
                    'turn': self.turn,
                    'currentTurnOwner': self.currentTurnOwner,
                    'effectOrder': self.effectOrder,
                    'effect': effect,
                    'effectOwner': effectOwner,
                    'land_hit':self.land_hit
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
                    'effectOwner': effectOwner,
                    'land_hit':self.land_hit
                })
            case EffectType.RANGE_BUFF:
                g_state_manager.Change(SelectionState.BUFF, {
                    'player': self.player,
                    'enemy': self.enemy,
                    'field': self.field,
                    'turn': self.turn,
                    'currentTurnOwner': self.currentTurnOwner,
                    'effectOrder': self.effectOrder,
                    'effect': effect,
                    'effectOwner': effectOwner,
                    'land_hit':self.land_hit
                })
            case EffectType.SELF_BUFF:
                buff = self.getBuffFromEffect(effect)
                print(f'{effectOwner.name} self buff: {buff.name}')
                if effectOwner == PlayerType.PLAYER:
                    self.player.add_buff(buff)
                elif effectOwner == PlayerType.ENEMY:
                    self.enemy.add_buff(buff)
            case EffectType.PUSH:
                pass
            case EffectType.PULL:
                pass
            case EffectType.CLEANSE:
                pass
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
                    'effectOwner': effectOwner,
                    'land_hit':self.land_hit
                })
            case EffectType.BLOOD_SACRIFICE:
                hp_paid = math.floor(self.player.health * 0.3)
                self.player.health -= hp_paid
                buff = self.getBuffFromEffect(effect)
                buff.value[0] = hp_paid
                self.player.add_buff(buff)
            case EffectType.ATTACK_BUFF: # if attack land then buff
                if self.currentTurnOwner == PlayerType.PLAYER and self.land_hit[PlayerType.PLAYER.value]:
                    buff = self.getBuffFromEffect(effect)
                    print(f'{effectOwner.name} self buff: {buff.name}')
                    self.player.add_buff(buff)
                elif self.currentTurnOwner == PlayerType.ENEMY and self.land_hit[PlayerType.ENEMY.value]:
                    buff = self.getBuffFromEffect(effect)
                    print(f'{effectOwner.name} self buff: {buff.name}')
                    self.enemy.add_buff(buff)
            case EffectType.CRITICAL:
                pass
            case EffectType.TRUE_DAMAGE:
                pass
            case EffectType.NEXT_MULTI:
                pass
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

    def getBuffFromEffect(self, effect):
        if effect.buffName:
            print(effect.buffName)
            return Buff(CARD_BUFF[effect.buffName])
        else:
            print(f'Buff not found: {effect.buffName}')
            return False

    def render(self, screen):
        RenderTurn(screen, 'Resolve State', self.turn, self.currentTurnOwner)
        RenderEntityStats(screen, self.player, self.enemy)
        RenderSelectedCard(screen, self.player.selectedCard, self.enemy.selectedCard)

        # Render field
        for fieldTile in self.field:
            fieldTile.render(screen, len(self.field))