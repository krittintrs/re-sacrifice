import pygame
from src.dependency import *

class FieldTile:
    def __init__(self, index, position):
        self.index = index  
        self.x, self.y = position
        self.entity = None  
        self.color = (0,0,0)
        self.solid = 1

    def is_occupied(self):
        return self.entity is not None

    def place_entity(self, entity, target_x):
        if not self.is_occupied():  
            self.entity = entity
            entity.field_index = self.index 
            if target_x == entity.x:
                print(f'{entity.name} is idle')
                entity.facing_left = False if entity.name == "player" else True

    def remove_entity(self):
        self.entity = None

    def render(self, screen):        
        # Draw the fieldTile
        rect = pygame.Rect(self.x, self.y, FIELD_WIDTH, FIELD_HEIGHT)
        pygame.draw.rect(screen, self.color, rect, self.solid)  

        # Render the entity if present
        if self.entity:
            self.entity.render(screen, rect.x, rect.y)
            for buff in self.entity.buffs:
                if buff.is_active():
                    buff.render(screen)