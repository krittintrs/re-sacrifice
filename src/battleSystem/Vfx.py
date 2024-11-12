from src.dependency import *


class Vfx:
    def __init__(self, animation_list, x, y):
        self.animation_list = animation_list
        self.curr_animation = None
        self.frame_index = 0
        self.frame_timer = 0
        self.finish = True
        self.x = x
        self.y = y
        self.animation_order = []

    def update(self, dt, x, y):
        self.x = x
        self.y = y
        if len(self.animation_order) != 0 and self.finish:
            self.curr_animation = self.animation_order.pop(0)
            self.finish = False
        # else:
        #     self.curr_animation = None

        if self.curr_animation is not None:
            if self.curr_animation in self.animation_list:
                vfxAnimation = self.animation_list[self.curr_animation]
                vfxAnimation.update(dt)
                if vfxAnimation.is_finished():
                    self.finish = True
                    if len(self.animation_order) == 0:
                        self.curr_animation = None
            

    def render(self, screen):
        if self.curr_animation is not None:
            if self.animation_list and self.curr_animation in self.animation_list:
                vfxAnimation = self.animation_list[self.curr_animation]
                vfxAnimation.render(screen, self.x - self.offset_x, self.y - self.offset_y)


    def play(self, name):
        # self.curr_animation = name
        self.animation_order.append(name)
        self.frame_index = 0
        self.offset_x = offset_x
        self.offset_y = offset_y
