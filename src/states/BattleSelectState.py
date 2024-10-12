import pygame
import sys
from src.dependency import *
from src.cardSystem.Card import Card
from src.cardSystem.Field import Field
from src.cardSystem.Entity import Entity

class BattleSelectState(BaseState):
    def __init__(self):
        super(BattleSelectState, self).__init__()

    def Exit(self):
        pass

    def Enter(self, param):
        # Retrieve the cards, entities, and fields from the parameter
        self.cards = param['cards']
        self.entities = param['entities']
        self.fields = param['fields']  # Get the fields from the previous state

    def render(self, screen):
        # Title
        screen.blit(pygame.font.Font(None, 36).render("Select Your Action: Press Escape to Exit", True, (255, 255, 255)), (10, SCREEN_HEIGHT - HUD_HEIGHT + 10))   

        # Mockup render cards
        for order, card in enumerate(self.cards):
            c = Card("card", "description","image", 1, 1, 1,1)
            c.render(screen, order)

        # Render fields
        for field in self.fields:
            field.render(screen, len(self.fields))

        # Render entities (if needed)
        for entity in self.entities:
            # Assuming entities are placed in their respective fields
            field = self.fields[entity.field_index]  # Get the field where the entity is located
            field.render(screen, len(self.fields))  # Render the field, which will render the entity inside it

    def update(self, dt, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                # Additional logic for handling actions in select state can be added here
