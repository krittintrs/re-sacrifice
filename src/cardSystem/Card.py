import pygame
from src.dependency import *

class Card:
    def __init__(self, name, description, cost, image):
        self.name = name
        self.description = description
        self.cost = cost
        self.image = image

    def render(self, screen, order):
        # Transparent card rendering at the bottom
        start_x = 80 + order * (CARD_WIDTH + 30)  # Space cards with 30px gap
        start_y = screen.get_height() - CARD_HEIGHT - 10  # Place near the bottom
        
        # Draw the border around the card
        pygame.draw.rect(screen, (0, 0, 0), (start_x, start_y, CARD_WIDTH, CARD_HEIGHT), 1)

    def update(self, dt, events):
        pass
