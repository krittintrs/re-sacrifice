import pygame
from src.dependency import *

class FieldTile:
    def __init__(self, index, position):
        self.index = index  
        self.x, self.y = position
        self.entity = None
        self.second_entity = None
        self.color = (0,0,0)
        self.solid = 1

    def is_occupied(self):
        if self.entity:
            return True
        else:
            return False

    def is_second_entity(self):
        if self.second_entity:
            return True
        else:
            return False

    def place_entity(self, entity, target_x):
        if entity.is_occupied_field:
            if not self.is_occupied():  
                self.entity = entity
                entity.field_index = self.index 
                if target_x == entity.x:
                    print(f'{entity.name} is idle')
                    entity.facing_left = False if entity.name == "player" else True
        else:
            if not self.is_second_entity():
                print("---------- assign", entity, "to second entity -------------")
                self.second_entity = entity
                entity.field_index = self.index 
                if target_x == entity.x:
                    print(f'{entity.name} is idle')
                    entity.facing_left = False if entity.name == "player" else True

    def remove_entity(self):
        self.entity = None

    def remove_second_entity(self):
        self.second_entity = None

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
        
        if self.second_entity:
            self.second_entity.render(screen, rect.x, rect.y + 40)