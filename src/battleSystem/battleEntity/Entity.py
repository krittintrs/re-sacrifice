import pygame
from src.dependency import *
from src.battleSystem.Deck import Deck

class Entity:
    def __init__(self, name, animation_list=None, health=10, image=None):
        self.name = name
        self.fieldTile_index = None  # Keep track of which field it is on
        self.image = image
        self.animation_list = animation_list
        self.curr_animation = "idle"  # Start with the idle animation
        self.frame_index = 0  # Frame index for animations
        self.frame_timer = 0  # Timer to manage frame rate
        self.frame_duration = 0.1  # Duration for each frame (adjust as needed)

        # Deck & Card
        self.deck = Deck()
        self.cardsOnHand = []
        self.selectedCard = None

        # Entity Stats
        self.health = health
        self.stunt = False
        self.buffs = [] # list of buff (or debuff?) apply on entity

    def print_stats(self):
        print(f'{self.name} stats - HP: {self.health}, ATK: {self.attack}, DEF: {self.defense}, SPD: {self.speed}, RNG: {self.range}')

    def print_buffs(self):
        for buff in self.buffs:
            buff.print()

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
    
    def apply_buffs_to_cardsOnHand(self):
        for card in self.cardsOnHand:
            card.reset_stats()
            for buff in self.buffs:
                if buff.is_active():
                    buff.apply(card)

    def select_card(self, card):
        print(f'\t{self.name} selected card: {card.name}')
        self.selectedCard = card
        self.selectedCard.isSelected = True

    def next_turn(self):
        # remove selected card and draw new card
        self.cardsOnHand.remove(self.selectedCard)
        self.selectedCard = None
        self.cardsOnHand.append(self.deck.draw(1)[0])

        # count down buffs
        for buff in self.buffs:
            buff.next_turn()

        # remove expired buffs
        for buff in self.buffs:
            if not buff.is_active():
                self.buffs.remove(buff)
 
    def select_position(self, index): 
        self.index = index

    def render(self, screen, x, y, color=(255, 0, 0)):
        # Define entity size
        entity_width, entity_height = 80, 80  # Example entity size
        
        # Calculate centered position within the field
        entity_x = x + (FIELD_WIDTH - entity_width) // 2  # Center horizontally
        entity_y = y + (FIELD_HEIGHT - entity_height) // 2  # Center vertically
        
        # Update animation frame
        if self.animation_list and self.curr_animation in self.animation_list:
            # Retrieve frames from the animation object
            animation = self.animation_list[self.curr_animation]
            animation_frames = animation.get_frames()
            
            if animation_frames:
                # Update frame index based on the timer
                self.frame_timer += 0.015  # Increase by seconds elapsed
                if self.frame_timer >= self.frame_duration:
                    self.frame_timer = 0
                    self.frame_index = (self.frame_index + 1) % len(animation_frames)
                
                # Render current animation frame
                current_frame = animation_frames[self.frame_index]
                screen.blit(current_frame, (entity_x - 55, entity_y - 20))
        else:
            pygame.draw.rect(screen, color, (entity_x, entity_y, entity_width, entity_height))
        
        # Render Buff Icons
        for index, buff in enumerate(self.buffs):
            buff.x = entity_x + index * 20
            buff.render(screen)

    def ChangeAnimation(self, name):
        print(f'{self.name} changing animation to {name}')
        if name in self.animation_list:
            self.curr_animation = name
            self.frame_index = 0
            self.frame_timer = 0
        else:
            print(f'Animation {name} not found in animation list for {self.name}')

