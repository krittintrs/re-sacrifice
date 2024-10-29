import pygame
from src.dependency import *
from src.battleSystem.Deck import Deck

class Entity:
    def __init__(self, name, health = 10, image=None):
        # For Render
        self.name = name
        self.fieldTile_index = None  # Keep track of which field it is on
        self.image = image

        # Deck & Card
        self.deck = Deck()
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
        for buff in self.buffs:
            if buff.is_active():
                buff.apply(self)

    def select_card(self, card):
        print(f'\t{self.name} selected card: {card.name}')
        self.selectedCard = card
        self.selectedCard.isSelected = True

        # self.attack = card.attack
        # self.defense = card.defense
        # self.speed = card.speed
        # self.range = card.range

    def next_turn(self):
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
            buff.next_turn()
            if not buff.is_active():
                self.buffs.remove(buff)
 
    def select_position(self, index): 
        self.index = index

    def render(self, screen, x, y, color=(255,0,0)):
        # Define entity size
        entity_width, entity_height = 80, 80  # Example entity size
        
        # Calculate centered position within the field
        entity_x = x + (FIELD_WIDTH - entity_width) // 2  # Center horizontally
        entity_y = y + (FIELD_HEIGHT - entity_height) // 2  # Center vertically

        # Render the entity (you can customize this)
        pygame.draw.rect(screen, color, (entity_x, entity_y, entity_width, entity_height))  # Red square as placeholder

        # Render Buff Icon
        for index, buff in enumerate(self.buffs):
            if buff.image is not None:
                buff.x = entity_x + index * 20
                buff.y = 100
                screen.blit(buff.image, (buff.x, 100))

                # try to render buff icon border
                pygame.draw.rect(screen, (0, 0, 0), (buff.x, buff.y, buff.rect.width, buff.rect.height), 1)

    def update(self, dt, events):
        pass
