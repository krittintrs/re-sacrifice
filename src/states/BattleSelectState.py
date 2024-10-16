import pygame
import sys
from src.dependency import *
from src.cardSystem.Card import Card
from src.cardSystem.Field import Field
from src.cardSystem.Entity import Entity

class BattleSelectState(BaseState):
    def __init__(self):
        super(BattleSelectState, self).__init__()
        self.selected_card = 0

    def Exit(self):
        pass

    def Enter(self, param):
        # Retrieve the cards, entities, and fields from the parameter
        self.cards = param['cards']
        self.entities = param['entities']
        self.fields = param['fields']
        self.dice = param['dice']

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
                    self.selected_card = (self.selected_card - 1) % len(self.cards)
                if event.key == pygame.K_RIGHT:
                    self.selected_card = (self.selected_card + 1) % len(self.cards)
                if event.key == pygame.K_RETURN:
                    g_state_manager.Change("action", {
                        'cards': self.cards,
                        'entities': self.entities,
                        'fields': self.fields,
                        'dice': self.dice,
                        'selected_card': self.selected_card
                    })

    def render(self, screen):
        # Title
        screen.blit(pygame.font.Font(None, 36).render("Select Your Action: Press Enter to Confirm", True, (255, 255, 255)), (10, SCREEN_HEIGHT - HUD_HEIGHT + 10))   

        # render cards
        for order, card in enumerate(self.cards):
            card.render(screen, order)
            card.render_selected(screen, self.selected_card)

        # Render fields
        for field in self.fields:
            field.render(screen, len(self.fields))

        # Render entities (if needed)
        for entity in self.entities:
            # Assuming entities are placed in their respective fields
            field = self.fields[entity.field_index]  # Get the field where the entity is located
            field.render(screen, len(self.fields))  # Render the field, which will render the entity inside it
