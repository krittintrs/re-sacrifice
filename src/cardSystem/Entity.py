import pygame
from src.dependency import *

class Entity:
    def __init__(self, name, health = 10, image=None):
        # For Render
        self.name = name
        self.fieldTile_index = None  # Keep track of which field it is on
        self.image = image

        # Deck & Card
        self.deck = []
        self.cardsOnHand = []
        self.selectedCard = None

        # Entity Stats
        self.health = health
        self.attack = 0
        self.defense = 0
        self.speed = 0
        self.range = 0
        self.stunt = False
        self.buffs = [] # list of buff (or debuff?) apply on entity

    def print_stats(self):
        print(f'{self.name} stats - HP: {self.health}, ATK: {self.attack}, DEF: {self.defense}, SPD: {self.speed}, RNG: {self.range}')

    def move_to(self, fieldTile, field):
        if fieldTile.is_occupied():  # Check if the fieldTile is occupied
            print("fieldTile is already occupied!")
            return

        # Remove from the current fieldTile if necessary
        if self.fieldTile_index is not None:
            field[self.fieldTile_index].remove_entity()  # Remove from current fieldTile
            
        fieldTile.place_entity(self)  # Place the entity in the new fieldTile
        self.fieldTile_index = fieldTile.index  # Update the fieldTile index

    def add_buff(self, buff):
        self.buffs.append(buff)
    
    def apply_existing_buffs(self):
        # self.print_stats()
        for buff in self.buffs:
            buff.apply(self)
        # self.print_stats()

    def select_card(self, card):
        print(f'\t{self.name} selected card: {card.name}')
        self.selectedCard = card
        self.selectedCard.isSelected = True

        self.attack = card.attack
        self.defense = card.defense
        self.speed = card.speed
        self.range = card.range

    def reset(self):
        # remove selected card and draw new card
        self.cardsOnHand.remove(self.selectedCard)
        self.selectedCard = None
        self.cardsOnHand.append(self.deck.draw(1)[0])

        # reset stats
        self.attack = 0
        self.defense = 0
        self.speed = 0
        self.range = 0

        # reset buffs
        for buff in self.buffs:
            buff.turn_passed()
 
    def select_position(self, index): 
        self.index = index

    def turn_pass(self):
        for buff in self.buffs:
            if not buff.is_active():
                self.buffs.remove(buff)

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
