import pygame
from src.dependency import *
from src.battleSystem.battleEntity.Entity import Entity
import tween
from src.battleSystem.Buff import Buff

# Define the global font variable
# You can adjust the font size and type as needed
g_font = pygame.font.Font(None, 36)


class SubEntity(Entity):
    def __init__(self, conf, side = PlayerType.PLAYER):
        super().__init__(conf.name,conf.animation_list, conf.health, conf.is_occupied_field)
        self.x, self.y = 0, ENTITY_Y
        self.attack = conf.attack
        self.duration = conf.duration
        self.range = conf.range
        self.side = side

    def print_stats(self):
        print(f'{self.name} stats - HP: {self.health}, ATK: {self.attack}')

    def display_stats(self):
        pass

    def reset_stats(self):
        pass

    def print_buffs(self):
        pass

    def move_to(self, fieldTile, field):
        pass

    def add_buff(self, buffList):
        pass
       
    def apply_buffs_to_cardsOnHand(self):
        pass

    def select_card(self, card):
        pass

    def remove_selected_card(self):
        pass

    def next_turn(self):
        pass # should implement something ?

    def select_position(self, index):
        self.index = index

    def collide(self, target, field):
        if self.name == "trap":
            if target.type != self.side:
                buff = Buff(CARD_BUFF["fire"])
                target.add_buff(buff)
                field.remove_second_entity()

    def bot_action(self, field):
        if self.attack != 0:
            for tile in field[self.index - self.range :  self.index + self.range + 1]:
                if tile.is_occupied() and tile.entity.type != self.side:
                    # should render attack animation here
                    damage = self.attack - tile.entity.defense
                    if damage > 0:
                        # ATTACK HIT
                        tile.entity.ChangeAnimation("death")
                        gSounds['attack'].play()
                        tile.entity.health -= damage
                        print(f'{tile.entity} takes {damage} damage')



    def update(self, dt):
        super().update(dt)
        # # Update the tween if it exists
        # if self.tweening:
        #     self.tweening._update(dt)  # Tween progress

        # if self.target_position == self.x:
        #     self.facing_left = False if self.name == "player" else True

        # # Check if an animation is set and update it
        # if self.curr_animation in self.animation_list:
        #     animation = self.animation_list[self.curr_animation]
        #     animation.update(dt)  # Progress the animation with delta time

        #     # If the animation has finished, switch to the idle animation
        #     if animation.is_finished() and self.curr_animation != "idle":
        #         self.ChangeAnimation("idle")

    def render(self, screen, x, y, color=(255, 0, 0)):
        super().render(screen, x, y, color)
        # # Use tweened x, y position if tween is in progress
        # render_x, render_y = (self.x, self.y) if self.tweening else (x, y)

        # # Define entity size
        # entity_width, entity_height = 80, 80  # Example entity size

        # # Calculate centered position within the field
        # # Center horizontally
        # entity_x = render_x + (FIELD_WIDTH - entity_width) // 2
        # # Center vertically
        # entity_y = render_y + (FIELD_HEIGHT - entity_height) // 2

        # # Define adjustable offsets for player and enemy
        # offset_x = -55 if self.name == 'player' else -185
        # offset_y = -20 if self.name == 'player' else -185

        # # Update animation frame
        # if self.animation_list and self.curr_animation in self.animation_list:
        #     # Retrieve frames from the animation object
        #     animation = self.animation_list[self.curr_animation]
        #     animation_frames = animation.get_frames()

        #     # Check if the animation has finished and switch to idle if necessary
        #     if animation.is_finished() and self.curr_animation != "idle":
        #         # Automatically switch to idle animation
        #         self.ChangeAnimation("idle")
        #         # Update to idle animation
        #         animation = self.animation_list[self.curr_animation]
        #         animation_frames = animation.get_frames()  # Update frames

        #     if animation_frames:
        #         # Update frame index based on the timer
        #         self.frame_timer += 0.01  # Increase by seconds elapsed
        #         if self.frame_timer >= self.frame_duration:
        #             self.frame_timer = 0
        #             self.frame_index = (
        #                 self.frame_index + 1) % len(animation_frames)

        #         # Render current animation frame with offsets applied
        #         current_frame = animation_frames[self.frame_index]
        #         screen.blit(
        #             pygame.transform.flip(
        #                 current_frame, self.facing_left, False),
        #             (entity_x + offset_x, entity_y + offset_y)
        #         )

        # else:
        #     # Placeholder red rectangle if no animation is provided
        #     pygame.draw.rect(
        #         screen, color, (entity_x, entity_y, entity_width, entity_height))

        # # Render Buff Icons
        # for index, buff in enumerate(self.buffs):
        #     buff.x = entity_x + index * 20
        #     buff.render(screen)

    def ChangeAnimation(self, name):
        super().ChangeAnimation(name)
    #     if name in self.animation_list:
    #         self.curr_animation = name
    #         self.frame_index = 0
    #         self.frame_timer = 0
    #         # Start from the beginning of the new animation
    #         self.animation_list[name].Refresh()
    #         print(f'{self.name} animation changed to {name}')
    #     else:
    #         print(
    #             f'Animation {name} not found in animation list for {self.name}')
