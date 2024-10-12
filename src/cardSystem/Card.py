import pygame
from src.dependency import *

class Card:
    def __init__(self, name, description, image, speed, dmg, defend, range):
        self.name = name
        self.description = description
        self.image = image
        self.speed = speed
        self.dmg = dmg
        self.defend = defend
        self.range = range

    def start(self, entity, enemy, field):
        # Perform card action
        pass

    def before(self, entity, enemy, field):
        # Perform card action before the main action
        pass

    def damage(self, entity, enemy, field):
        # Perform card action for damage
        pass

    def end(self, entity, enemy, field):
        # Perform card action at the end
        pass

    def render(self, screen, order):
        # Transparent card rendering at the bottom
        start_x = 80 + order * (CARD_WIDTH + 30)  # Space cards with 30px gap
        start_y = SCREEN_HEIGHT - CARD_HEIGHT - 10  # Place near the bottom
        
        # Draw the border around the card
        pygame.draw.rect(screen, (0, 0, 0), (start_x, start_y, CARD_WIDTH, CARD_HEIGHT), 1)

    def update(self, dt, events):
        pass
