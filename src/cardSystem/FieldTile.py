import pygame
from src.dependency import *

class FieldTile:
    def __init__(self, index, position):
        self.index = index  # Index in the row
        self.position = position  # (x, y) coordinates for rendering
        self.entity = None  # Store the entity occupying the fieldTile

    def is_occupied(self):
        return self.entity is not None

    def place_entity(self, entity):
        if not self.is_occupied():  # Only place if the fieldTile is empty
            self.entity = entity
            entity.field_index = self.index  # Update entity's fieldTile index

    def remove_entity(self):
        self.entity = None

    def render(self, screen, total_fieldTile):        
        # Calculate total width of all fieldTile including FIELD_GAP
        total_width = total_fieldTile * FIELD_WIDTH + (total_fieldTile - 1) * FIELD_GAP

        # Calculate starting x-coordinate to center of the field
        start_x = (SCREEN_WIDTH - total_width) // 2
        y = SCREEN_HEIGHT // 3 - FIELD_HEIGHT // 2

        # Draw the fieldTile
        rect = pygame.Rect(start_x + self.index * (FIELD_WIDTH + FIELD_GAP), y, FIELD_WIDTH, FIELD_HEIGHT)
        pygame.draw.rect(screen, (0, 0, 0), rect, 1)  # fieldTile outline

        # Render the entity if present
        if self.entity:
            self.entity.render(screen, rect.x, rect.y)