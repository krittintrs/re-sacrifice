from src.constants import *
from src.rpg.entity.EntityWalkState import EntityWalkState
import pygame, time

class PlayerWalkState(EntityWalkState):
    def __init__(self, player):
        super(PlayerWalkState, self).__init__(player)

        self.entity.ChangeAnimation('down')

    def Exit(self):
        pass

    def Enter(self, params):
        "Enter Walk"
        self.entity.offset_y = 15
        self.entity.offset_x = 0
        super().Enter(params)

    def update(self, dt, events):
        pressedKeys = pygame.key.get_pressed()
        if pressedKeys[pygame.K_LEFT]:
            self.entity.direction = 'left'
            self.entity.ChangeAnimation('left')
        elif pressedKeys[pygame.K_RIGHT]:
            self.entity.direction = 'right'
            self.entity.ChangeAnimation('right')
        elif pressedKeys[pygame.K_DOWN]:
            self.entity.direction = 'down'
            self.entity.ChangeAnimation('down')
        elif pressedKeys[pygame.K_UP]:
            self.entity.direction = 'up'
            self.entity.ChangeAnimation('up')
        else:
            self.entity.ChangeState('idle')

        # for event in events:
        #     if event.type == pygame.KEYDOWN:
        #         if event.key == pygame.K_SPACE:
        #             self.entity.ChangeState('swing_sword'

        #move and bump to the wall check
        super().update(dt, events)