from src.states.BaseState import BaseState
from src.dependency import *
from src.constants import *
import pygame
import sys

class BattleResolveState(BaseState):
    def __init__(self):
        super(BattleResolveState, self).__init__()

    def Enter(self, params):
        print(">>>>>> Enter BattleResolveState <<<<<<")
        self.player = params['player']
        self.enemy = params['enemy']
        self.field = params['field']
        self.turn = params['turn']
        self.currentTurnOwner = params['currentTurnOwner']  
        self.effectOrder = params['effectOrder']

        # self.player.print_stats()
        # self.enemy.print_stats()
        print(f'effectOrder: {self.effectOrder}')

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
        # Turn
        screen.blit(pygame.font.Font(None, 36).render(f"Resolve Phase - Turn {self.turn}", True, (0, 0, 0)), (10, 10))   

        # Render cards on player's hand
        for order, card in enumerate(self.player.cardsOnHand):
            card.render(screen, order)

        # Render field
        for fieldTile in self.field:
            fieldTile.render(screen, len(self.field))