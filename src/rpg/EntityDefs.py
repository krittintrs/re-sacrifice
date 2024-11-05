from src.constants import *
from src.rpg.Resources import *
class EntityConf:
    def __init__(self, animation, walk_speed=60, x=None, y=None, width=48, height=48, health=1, offset_x=0, offset_y=0):
        self.animation = animation
        self.walk_speed = walk_speed

        self.x = x
        self.y = y

        self.width = width
        self.height = height

        self.health = health

        self.offset_x = offset_x
        self.offset_y = offset_y


ENTITY_DEFS = {
    'player': EntityConf(animation=gPlayer_animation_list, walk_speed=PLAYER_WALK_SPEED,
                         x=1024//2, y=1024//2, width=32, height=44,
                         health=6, offset_x=0, offset_y=0)
}