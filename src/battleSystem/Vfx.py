from src.dependency import *


class Vfx:
    def __init__(self, animation_list, x, y):
        self.animation_list = animation_list
        self.curr_animation = None
        self.frame_index = 0
        self.frame_timer = 0
        self.x = x
        self.y = y

        self.offset_x = 20
        self.offset_y = 0

    def update(self, dt, x, y):
        self.x = x
        self.y = y
        if self.curr_animation is not None:
            if self.curr_animation in self.animation_list:
                vfxAnimation = self.animation_list[self.curr_animation]
                vfxAnimation.update(dt)
            

    def render(self, screen):
        if self.curr_animation is not None:
            if self.animation_list and self.curr_animation in self.animation_list:
                vfxAnimation = self.animation_list[self.curr_animation]
                vfxAnimation.render(screen, self.x - self.offset_x, self.y - self.offset_y)

    def play(self, name, offset_x=0, offset_y=0):
        self.curr_animation = name
        self.frame_index = 0
        self.offset_x = offset_x
        self.offset_y = offset_y
