from src.states.BaseState import BaseState
from src.dependency import *
from src.constants import *
import pygame,sys

class BattleInitialState(BaseState):
    def __init__(self):
        super(BattleInitialState, self).__init__()

    def Exit(self):
        pass

    def Enter(self, param):
        pass 

    def render(self, screen):
        pass

    def update(self, dt, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()