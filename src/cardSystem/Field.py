import pygame
from src.dependency import *

class Field:
    def __init__(self, index, position):
        self.index = index  # Index in the row
        self.position = position  # (x, y) coordinates for rendering
        self.entity = None  # Store the entity occupying the field

    def is_occupied(self):
        return self.entity is not None

    def place_entity(self, entity):
        if not self.is_occupied():  # Only place if the field is empty
            self.entity = entity
            entity.field_index = self.index  # Update entity's field index

    def remove_entity(self):
        self.entity = None

    def render(self, screen, total_fields):        
        # Calculate total width of all fields including FIELD_GAP
        total_width = total_fields * FIELD_WIDTH + (total_fields - 1) * FIELD_GAP

        # Calculate starting x-coordinate to center fields
        start_x = (SCREEN_WIDTH - total_width) // 2
        y = SCREEN_HEIGHT // 3 - FIELD_HEIGHT // 2

        # Draw the field
        rect = pygame.Rect(start_x + self.index * (FIELD_WIDTH + FIELD_GAP), y, FIELD_WIDTH, FIELD_HEIGHT)
        pygame.draw.rect(screen, (0, 0, 0), rect, 1)  # Field outline

        # Render the entity if present
        if self.entity:
            self.entity.render(screen, rect.x, rect.y)