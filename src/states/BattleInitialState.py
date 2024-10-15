from src.states.BaseState import BaseState
from src.dependency import *
from src.constants import *
from src.cardSystem.Card import Card
from src.cardSystem.Field import Field
from src.cardSystem.Entity import Entity
import pygame
import sys

import random


class BattleInitialState(BaseState):
    def __init__(self):
        super(BattleInitialState, self).__init__()
        self.cards = []
        self.entities = []

        # Create fields
        self.fields = self.create_fields(9)  # Create 9 fields in a single row

        # Mock up draw entities
        # Create an entity
        player = Entity("Player")        
        self.entities.append(player)
        player.move_to(self.fields[0], self.fields)  # Place player in the first field
        # Example: Move the player to another field (e.g., field at index 4)
        player.move_to(self.fields[4], self.fields)


    def Exit(self):
        pass

    def Enter(self, param):
        print("Enter BattleInitialState")

        self.deck = param['deck']
        self.cards = param['cards']

        for i in range(len(self.cards)):
            print("Card: ", self.cards[i].name)

    def update(self, dt, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_RETURN:
                    g_state_manager.Change("select", {
                        'cards': self.cards,
                        'entities': self.entities,
                        'fields': self.fields  # Pass the fields here
                    })


    def render(self, screen):
        # Title
        screen.blit(pygame.font.Font(None, 36).render("Cards:    Press Enter to Start", True, (255, 255, 255)), (10, SCREEN_HEIGHT - HUD_HEIGHT + 10))   
        
        # Mockup render cards
        for order, card in enumerate(self.cards):
            card.render(screen, order)

        # Render fields
        for field in self.fields:
            field.render(screen, len(self.fields))

    def create_fields(self, num_fields):
        fields = []
        for i in range(num_fields):
            x = i * 100  # Adjust the x position based on index
            y = 200  # Since you have only one row, y is constant
            fields.append(Field(i, (x, y)))  # Create and append each field
        return fields