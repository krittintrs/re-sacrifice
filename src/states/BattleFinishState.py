from src.states.BaseState import BaseState
from src.dependency import *
from src.constants import *
import pygame

class BattleFinishState(BaseState):
    def Enter(self, params):
        pass

    def Exit(self):
        pass

    def update(self, dt, events):
        # Update buff
        for buff in self.player.buffs:
            buff.update(dt, events)
        for buff in self.enemy.buffs:
            buff.update(dt, events)
            
        self.player.update(dt)

    def render(self, screen):
        pass