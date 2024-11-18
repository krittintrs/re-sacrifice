import random
import math
from src.states.BaseState import BaseState
from src.constants import *

class EntityWalkState(BaseState):
    def __init__(self, entity):
        self.entity = entity
        self.entity.ChangeAnimation('down')

        # AI control
        self.move_duration = 0
        self.movement_timer = 0

        # hit screen edge?
        self.bumped = False

    def update(self, dt, events):
        self.bumped = False  # Reset bumped status

        # Movement in free space without tile snapping
        if self.entity.direction == "left":
            #self.entity.MoveX(-self.entity.walk_speed * dt)
            if self.entity.rect.x <= 0:
                self.entity.ChangeCoord(x=0)
                self.bumped = True

        elif self.entity.direction == "right":
            #self.entity.MoveX(self.entity.walk_speed * dt)
            if self.entity.rect.x + self.entity.width >= SCREEN_WIDTH:
                self.entity.ChangeCoord(x=SCREEN_WIDTH - self.entity.width)
                self.bumped = True

        elif self.entity.direction == "up":
            #self.entity.MoveY(-self.entity.walk_speed * dt)
            if self.entity.rect.y <= 0:
                self.entity.ChangeCoord(y=0)
                self.bumped = True

        elif self.entity.direction == "down":
            #self.entity.MoveY(self.entity.walk_speed * dt)
            if self.entity.rect.y + self.entity.height >= SCREEN_HEIGHT:
                self.entity.ChangeCoord(y=SCREEN_HEIGHT - self.entity.height)
                self.bumped = True

        if self.entity.curr_animation.is_finished():
            self.entity.ChangeState("idle")

    def Enter(self, params):
        pass

    def Exit(self):
        pass

    def ProcessAI(self, params, dt):
        directions = ["left", "right", "up", "down"]

        # Randomly decide to change direction or switch to idle
        if self.move_duration == 0 or self.bumped:
            self.move_duration = random.uniform(1, 3)  # Set duration randomly for smooth AI movement
            self.entity.direction = random.choice(directions)
            self.entity.ChangeAnimation(self.entity.direction)

        elif self.movement_timer > self.move_duration:
            self.movement_timer = 0
            if random.randint(0, 3) == 1:  # 1 in 4 chance to switch to idle
                self.entity.ChangeState("idle")
            else:
                self.move_duration = random.uniform(1, 3)
                self.entity.direction = random.choice(directions)
                self.entity.ChangeAnimation(self.entity.direction)

        self.movement_timer += dt

    def render(self, screen):
        animation = self.entity.curr_animation.image
        # Draw entity without tile-based positioning
        print(self.entity.offset_x, self.entity.offset_y)
        screen.blit(animation, (
            math.floor(self.entity.rect.x - self.entity.offset_x),
            math.floor(self.entity.rect.y - self.entity.offset_y)
        ))
