from src.states.BaseState import BaseState
from src.dependency import *
from src.constants import *
import pygame
import sys

class SelectAttackState(BaseState):
    def __init__(self):
        super(SelectAttackState, self).__init__()

    def Enter(self, params):
        self.player = params['player']
        self.enemy = params['enemy']
        self.field = params['field']
        self.turn = params['turn']
        self.currentTurnOwner = params['currentTurnOwner']  
        self.effectOrder = params['effectOrder']
        self.effect = params['effect']
        self.effectOwner = params['effectOwner']

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
                    print('!!!! SelectAttackState !!!!')
                    print(f'Owner: {self.effectOwner}')
                    print(f'Effect: {self.effect.type} ({self.effect.minRange} - {self.effect.maxRange})')

                    g_state_manager.Change(BattleState.RESOLVE_PHASE, {
                        'player': self.player,
                        'enemy': self.enemy,
                        'field': self.field,
                        'turn': self.turn,
                        'currentTurnOwner': self.currentTurnOwner,
                        'effectOrder': self.effectOrder
                    })

    def render(self, screen):
        # Turn
        screen.blit(pygame.font.Font(None, 36).render(f"SelectAttackState - Turn {self.turn}", True, (0, 0, 0)), (10, 10))   

        # Render cards on player's hand
        for order, card in enumerate(self.player.cardsOnHand):
            card.render(screen, order)

        # Render field
        for fieldTile in self.field:
            fieldTile.render(screen, len(self.field))

        