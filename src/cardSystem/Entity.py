import pygame
from src.dependency import *

class Entity:
    def __init__(self, name, image=None):
        self.name = name
        self.field_index = None  # Keep track of which field it is on
        self.index = None
        self.deck = []
        self.hand = []
        self.selected_card = None
        self.stunt = False
        self.image = image

    def move_to(self, field, fields):
        if field.is_occupied():  # Check if the field is occupied
            print("Field is already occupied!")
            return

        # Remove from the current field if necessary
        if self.field_index is not None:
            current_field = fields[self.field_index]  # Access fields from the passed list
            current_field.remove_entity()  # Remove from current field

        field.place_entity(self)  # Place the entity in the new field

    def render(self, screen, x, y):
        # Define entity size
        entity_width, entity_height = 80, 80  # Example entity size
        
        # Calculate centered position within the field
        entity_x = x + (FIELD_WIDTH - entity_width) // 2  # Center horizontally
        entity_y = y + (FIELD_HEIGHT - entity_height) // 2  # Center vertically

        # Render the entity (you can customize this)
        pygame.draw.rect(screen, (255, 0, 0), (entity_x, entity_y, entity_width, entity_height))  # Red square as placeholder

    def update(self, dt, events):
        pass

class Player(Entity):
    def __init__(self, name, image=None):
        super().__init__(name, image)

    def update(self, dt, events):
        # Implement player-specific update logic here
        pass

    def render(self, screen, x, y):
        # Call the parent render method
        super().render(screen, x, y)
        # Add player-specific rendering logic here if needed
        pass

class Enemy(Entity):
    def __init__(self, name, image=None):
        super().__init__(name, image)
        self.health = 100  # Example additional attribute for Enemy
    
    def selectCard(self, card):
        self.selected_card = card

    def selectPosition(self, index):
        self.index = index

    def update(self, dt, events):
        # Implement enemy-specific update logic here
        pass

    def render(self, screen, x, y):
        # Call the parent render method
        super().render(screen, x, y)
        # Add enemy-specific rendering logic here if needed
        pass

class Boss(Enemy):
    def __init__(self, name, image=None):
        super().__init__(name, image)
        self.attack = 20  # Example additional attribute for Boss

    def update(self, dt, events):
        # Implement boss-specific update logic here
        pass

    def render(self, screen, x, y):
        # Call the parent render method
        super().render(screen, x, y)
        # Add boss-specific rendering logic here if needed
        pass
