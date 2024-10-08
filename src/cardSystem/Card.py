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
        start_x = order * (CARD_WIDTH + 10)  # Space cards with 10px gap
        start_y = screen.get_height() - CARD_HEIGHT - 10  # Place near the bottom

        # # Create a transparent surface for the card
        # transparent_surface = pygame.Surface((CARD_WIDTH, CARD_HEIGHT), pygame.SRCALPHA)
        # pygame.draw.rect(transparent_surface, (0, 255, 0, 100), (0, 0, CARD_WIDTH, CARD_HEIGHT))  # Semi-transparent green fill
        
        # # Blit the transparent card onto the screen
        # screen.blit(transparent_surface, (start_x, start_y))
        
        # Draw the border around the card
        pygame.draw.rect(screen, (0, 0, 0), (start_x, start_y, CARD_WIDTH, CARD_HEIGHT), 1)

    def update(self, dt, events):
        pass
