import math

from src.states.BaseState import BaseState
import random

class EntityIdleState(BaseState):
    def __init__(self, entity):
        self.entity = entity
        self.entity.ChangeAnimation(self.entity.direction)

        # monster AI waiting
        self.wait_duration = 0
        self.wait_timer = 0

    def Enter(self, params):
        self.entity.ChangeAnimation(self.entity.direction)

    def Exit(self):
        pass

    def update(self, dt, events):
        pass

    def ProcessAI(self, params, dt):
        if self.wait_duration == 0:
            self.wait_duration = random.randint(0, 5)
        else:
            self.wait_timer = self.wait_timer+dt

            if self.wait_timer > self.wait_duration:
                self.entity.ChangeState('walk')

    def render(self, screen):
        idle_image = self.entity.curr_animation.idleSprite

        screen.blit(idle_image, (math.floor(self.entity.rect.x - self.entity.offset_x),
                    math.floor(self.entity.rect.y - self.entity.offset_y)))