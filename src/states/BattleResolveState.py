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
        self.selected_card_index = params['selected_card_index']
        self.effectOrder = params['effectOrder']

        self.player.print_stats()
        self.enemy.print_stats()
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
        

    def render(self, screen):
        # Render cards on player's hand
        for order, card in enumerate(self.player.cardsOnHand):
            card.render(screen, order)
            card.render_selected(screen, self.selected_card_index)

        # Render field
        for fieldTile in self.field:
            fieldTile.render(screen, len(self.field))