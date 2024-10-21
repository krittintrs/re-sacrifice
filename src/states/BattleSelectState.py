import pygame
import sys
from src.dependency import *

class BattleSelectState(BaseState):
    def __init__(self):
        super(BattleSelectState, self).__init__()
        self.selected_index = 0

    def Enter(self, params):
        print(">>>>>> Enter BattleSelectState <<<<<<")
        # Retrieve the cards, entities, and field from the parameter
        self.player = params['player']
        self.enemy = params['enemy']
        self.field = params['field']
        self.turn = params['turn']
        self.currentTurnOwner = params['currentTurnOwner']  

        self.player.cardsOnHand[self.selected_index].isSelected = True

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
                    newIndex = (self.selected_index - 1) % len(self.player.cardsOnHand)
                    self.change_selection(newIndex)
                if event.key == pygame.K_RIGHT:
                    newIndex = (self.selected_index + 1) % len(self.player.cardsOnHand)
                    self.change_selection(newIndex)
                if event.key == pygame.K_RETURN:
                    selectedCard = self.player.cardsOnHand[self.selected_index]
                    self.player.select_card(selectedCard)
                    selectedCard.print_stats()
                    for card in self.player.cardsOnHand:
                        print(f'Player\'s Hand Card: {card.name}, isSelected: {card.isSelected}')
                    g_state_manager.Change(BattleState.ACTION_PHASE, {
                        'player': self.player,
                        'enemy': self.enemy,
                        'field': self.field,
                        'turn': self.turn,
                        'currentTurnOwner': self.currentTurnOwner,
                    })

    def change_selection(self, newIndex):
        self.player.cardsOnHand[self.selected_index].isSelected = False
        self.player.cardsOnHand[newIndex].isSelected = True
        self.selected_index = newIndex

    def render(self, screen):
        # Title
        screen.blit(pygame.font.Font(None, 36).render("Select Card: Press Enter to Confirm", True, (255, 255, 255)), (10, SCREEN_HEIGHT - HUD_HEIGHT + 10))   

        # Render cards on player's hand
        for order, card in enumerate(self.player.cardsOnHand):
            card.render(screen, order)

        # Render field
        for fieldTile in self.field:
            fieldTile.render(screen, len(self.field))

