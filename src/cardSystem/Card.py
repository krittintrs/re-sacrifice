import pygame
from src.dependency import *

class Card:
    def __init__(self, id, name, class_, type, description, image, attack, defense, speed, range_start, range_end, beforeEffect = [], mainEffect = [], afterEffect = []):
        # For Render
        self.id = id
        self.class_ = class_
        self.type = type
        self.name = name
        self.description = description
        self.image = image
        self.isSelected = False

        # Card Stats
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.range_start = range_start
        self.range_end = range_end

        # Card Effects
        self.beforeEffect = beforeEffect # list of Effects
        self.mainEffect = mainEffect
        self.afterEffect = afterEffect

    def print_stats(self):
        print(f'{self.name} stats - ATK: {self.attack}, DEF: {self.defense}, SPD: {self.speed}, RNG: {self.range_start}-{self.range_end}')
        
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

        # Draw the card image

        # Draw the card name
        screen.blit(pygame.font.Font(None, 24).render(self.name, True, (255, 255, 255)), (start_x + 10, start_y + 10))

        # Draw card modified numbers

        # if selected
        if self.isSelected:
            # Highlight the selected card by rendering a thicker border
            pygame.draw.rect(screen, (255, 255, 0), (start_x, start_y, CARD_WIDTH, CARD_HEIGHT), 3)

    # def render_selected(self, screen, selected_index):
    #     # Highlight the selected card by rendering a thicker border
    #     start_x = 80 + selected_index * (CARD_WIDTH + 30)
    #     start_y = SCREEN_HEIGHT - CARD_HEIGHT - 10
        
    #     # Draw the highlighted border around the card
    #     pygame.draw.rect(screen, (255, 255, 0), (start_x, start_y, CARD_WIDTH, CARD_HEIGHT), 3)

    def render_position(self, screen, position, scale):
        pygame.draw.rect(screen, (0,0,0), (position[0],position[1],CARD_WIDTH*scale, CARD_HEIGHT*scale), 1)

    def update(self, dt, events):
        pass
