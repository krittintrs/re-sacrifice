from src.states.BaseState import BaseState
from src.dependency import *
from src.constants import *
from src.Render import *
import pygame
import sys

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

        # For Debug Buffs
        print(f'Player Buffs: {self.player.buffs}')
        self.player.print_buffs()
        print(f'Enemy Buffs: {self.enemy.buffs}')
        self.enemy.print_buffs()

        # apply buff to all cards on hand
        self.player.apply_buffs_to_cardsOnHand()
        self.enemy.apply_buffs_to_cardsOnHand()

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
            g_state_manager.Change(BattleState.END_PHASE, {
                'player': self.player,
                'enemy': self.enemy,
                'field': self.field,
                'turn': self.turn,
                'currentTurnOwner': self.currentTurnOwner
            })
            
    # Update buff
        for buff in self.player.buffs:
            buff.update(dt, events)
        for buff in self.enemy.buffs:
            buff.update(dt, events)

    def resolveCardEffect(self, effect, effectOwner):
        if effect.type == EffectType.ATTACK:
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
        elif effect.type == EffectType.MOVE:
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
        elif effect.type == EffectType.RANGE_BUFF:
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
        elif effect.type == EffectType.SELF_BUFF:
            print(f'{effectOwner.name} self buff')

    def render(self, screen):
        RenderTurn(screen, 'Resolve State', self.turn, self.currentTurnOwner)
        RenderEntityStats(screen, self.player, self.enemy)

        # Render cards on player's hand
        for order, card in enumerate(self.player.cardsOnHand):
            card.render(screen, order)

        # Render field
        for fieldTile in self.field:
            fieldTile.render(screen, len(self.field))