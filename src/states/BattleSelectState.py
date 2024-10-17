import pygame
import sys
from src.dependency import *

class BattleSelectState(BaseState):
    def __init__(self):
        super(BattleSelectState, self).__init__()
        self.selected_card_index = 0

    def Enter(self, param):
        # Retrieve the cards, entities, and field from the parameter
        self.player = param['player']
        self.enemy = param['enemy']
        self.field = param['field']
        self.turn = param['turn']
        self.currentTurnOwner = param['currentTurnOwner']  

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
                if event.key == pygame.K_LEFT:
                    self.selected_card_index = (self.selected_card_index - 1) % len(self.player.cardsOnHand)
                if event.key == pygame.K_RIGHT:
                    self.selected_card_index = (self.selected_card_index + 1) % len(self.player.cardsOnHand)
                if event.key == pygame.K_RETURN:
                    g_state_manager.Change(BattleState.ACTION_PHASE, {
                        'player': self.player,
                        'enemy': self.enemy,
                        'field': self.field,
                        'turn': self.turn,
                        'currentTurnOwner': self.currentTurnOwner,
                        'selected_card_index': self.selected_card_index
                    })

    def render(self, screen):
        # Title
        screen.blit(pygame.font.Font(None, 36).render("Select Card: Press Enter to Confirm", True, (255, 255, 255)), (10, SCREEN_HEIGHT - HUD_HEIGHT + 10))   

        # Render cards on player's hand
        for order, card in enumerate(self.player.cardsOnHand):
            card.render(screen, order)
            card.render_selected(screen, self.selected_card_index)

        # Render field
        for fieldTile in self.field:
            fieldTile.render(screen, len(self.field))

