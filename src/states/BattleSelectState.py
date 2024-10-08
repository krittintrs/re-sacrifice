from src.states.BaseState import BaseState
from src.dependency import *
from src.constants import *
import pygame,sys
import random

class BattleSelectState(BaseState):
    def __init__(self):
        super(BattleSelectState, self).__init__()

    def Exit(self):
        pass

    def Enter(self, param):
        self.cards = param['cards']
        self.entities = param['entities']

    def render(self, screen):
        # Mock create cards layout
        for i in range(0, 5):
            self.cards.append(random.randint(0, 2))  # Random card setup

        print("cards: ", self.cards)
        for order, card in enumerate(self.cards):
            c = Card("card", "description", 1, "image")
            c.render(screen, order)  # Render cards based on their order (position)

    def update(self, dt, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()