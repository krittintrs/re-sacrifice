from src.rpg.EntityBase import EntityBase
from src.dependency import *
from src.StateMachine import StateMachine
class Player(EntityBase):
    def __init__(self, conf):
        self.offset_y = 100
        super(Player, self).__init__(conf)

    def update(self, dt, events):
        super().update(dt, events)


    def Collides(self, target):
        y, height = self.y, self.height
        
        return not (self.x + self.width < target.x or self.x > target.x + target.width or
                    y + height + 10 < target.y or y+20 > target.y + target.height)


    def render(self, screen, adjacent_offset_x=0, adjacent_offset_y=0):
        super().render(screen, adjacent_offset_x, adjacent_offset_y)

    def CreateAnimations(self):
        self.animation_list = gPlayer_animation_list