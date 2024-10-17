import pygame
from src.dependency import *

class Entity:
    def __init__(self, name, health = 10, image=None):
        self.name = name
        self.field_index = None  # Keep track of which field it is on
        self.index = None
        self.deck = []
        self.cardsOnHand = []
        self.selected_card = None
        self.buff = [] # list of buff (or debuff?) apply on entity
        self.health = health
        self.stunt = False
        self.image = image

    def move_to(self, fieldTile, field):
        if fieldTile.is_occupied():  # Check if the fieldTile is occupied
            print("fieldTile is already occupied!")
            return

        # Remove from the current fieldTile if necessary
        if self.field_index is not None:
            current_field = field[self.field_index]  # Access field from the passed list
            current_field.remove_entity()  # Remove from current fieldTile

        fieldTile.place_entity(self)  # Place the entity in the new fieldTile

    def add_buff(self, buff):
        self.buff.append(buff)

    def get_speed(self):
        if self.selected_card:
            spd = self.selected_card.speed
            for buff in self.buff:
                spd += buff.value[2]
            return spd
        else:
            print("these is no selected card")
            return
        
    def select_card(self, card):
        self.selected_card = card

    def select_position(self, index): 
        self.index = index

    def turn_pass(self):
        for buff in self.buff:
            if not buff.is_active():
                self.buff.remove(buff)
        

    def render(self, screen, x, y, color=(255,0,0)):
        # Define entity size
        entity_width, entity_height = 80, 80  # Example entity size
        
        # Calculate centered position within the field
        entity_x = x + (FIELD_WIDTH - entity_width) // 2  # Center horizontally
        entity_y = y + (FIELD_HEIGHT - entity_height) // 2  # Center vertically

        # Render the entity (you can customize this)
        pygame.draw.rect(screen, color, (entity_x, entity_y, entity_width, entity_height))  # Red square as placeholder

    def update(self, dt, events):
        pass

class Player(Entity):
    def __init__(self, name, image=None):
        super().__init__(name, image)
        self.health = 30

    def update(self, dt, events):
        # Implement player-specific update logic here
        pass

    def render(self, screen, x, y):
        # Call the parent render method
        super().render(screen, x, y, (0,255,0))
        # Add player-specific rendering logic here if needed
        pass

class Enemy(Entity):
    def __init__(self, name, image=None):
        super().__init__(name, image)
        self.health = 100  # Example additional attribute for Enemy

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
