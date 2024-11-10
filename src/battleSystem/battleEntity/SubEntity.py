import pygame
from src.dependency import *
from src.battleSystem.battleEntity.Entity import Entity
import tween
from src.battleSystem.Buff import Buff

# Define the global font variable
# You can adjust the font size and type as needed
g_font = pygame.font.Font(None, 36)


class SubEntity(Entity): # these sub entity will attack every round if attack != 0
    def __init__(self, conf, side = PlayerType.PLAYER):
        super().__init__(conf.name,conf.animation_list, conf.health, conf.is_occupied_field)
        self.x, self.y = 0, ENTITY_Y
        self.attack = conf.attack # default attack
        self.duration = conf.duration # remove if duration reach 0
        self.range = conf.range # range for attacking
        self.side = side # player or enemy side (base on who summon)
        self.remove_flag = False # remove flag is for removing itself after finishing animation

    def next_turn(self):
        self.duration -= 1
        if self.duration == 0:
            return True
        else:
            return False

    def select_position(self, index):
        self.index = index
    
    def take_damage(self, damage):
        self.health -= damage
        if self.health > 0:
            self.ChangeAnimation("death")
        else:
            self.ChangeAnimation("death", True)

    def remove_self(self):
        self.duration = 0

    def collide(self, target):
        if self.name == "trap":
            if target.type != self.side:
                # mock animation
                buff = Buff(CARD_BUFF["fire"])
                target.add_buff(buff)
                self.ChangeAnimation('attack', True)
                target.ChangeAnimation('death')
        if self.name == "attack summon":
            if target.type != self.side:
                target.health -= 1
                if target.type == PlayerType.ENEMY:
                    target.ChangeAnimation('death')
                    gSounds['attack'].play()
                self.ChangeAnimation('attack', True)

    def bot_action(self, field):
        if self.attack != 0:
            for tile in field[self.fieldTile_index - self.range :  self.fieldTile_index + self.range + 1]:
                if tile.is_occupied() and tile.entity.type != self.side:
                    damage = self.attack - tile.entity.defense
                    if damage > 0:
                        # ATTACK HIT
                        tile.entity.ChangeAnimation("death")
                        tile.entity.health -= damage
                        print(f'{tile.entity} takes {damage} damage')
                    gSounds['attack'].play()
                    self.ChangeAnimation("attack")
                    print("summon attack")



    def update(self, dt):
        if self.tweening:
            self.tweening._update(dt)  # Tween progress

        if self.target_position == self.x:
            self.facing_left = False if self.name == "player" else True

        # Check if an animation is set and update it
        if self.curr_animation in self.animation_list:
            animation = self.animation_list[self.curr_animation]
            animation.update(dt)  # Progress the animation with delta time

            # If the animation has finished, switch to the idle animation
            if animation.is_finished() and self.curr_animation != "idle":
                if self.remove_flag:
                    self.remove_self()
                self.ChangeAnimation("idle")

    def render(self, screen, x, y, color=(255, 0, 0)):
        super().render(screen, x, y, color)


    def ChangeAnimation(self, name, remove_flag = False):
        if name in self.animation_list:
            self.curr_animation = name
            self.frame_index = 0
            self.frame_timer = 0
            self.remove_flag = remove_flag
            # Start from the beginning of the new animation
            self.animation_list[name].Refresh()
            print(f'{self.name} animation changed to {name}')
        else:
            print(
                f'Animation {name} not found in animation list for {self.name}')
