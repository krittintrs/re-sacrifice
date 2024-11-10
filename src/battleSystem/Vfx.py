from src.dependency import *

class Vfx:
    def __init__(self, animation_list, x, y):
        self.animation_list = animation_list
        self.curr_animation = ""
        self.frame_index = 0
        self.frame_timer = 0
        self.frame_duration = 0.1
        self.x = x
        self.y = y

    def update(self, dt):
        self.frame_timer += dt
        if self.frame_timer >= self.frame_duration:
            self.frame_timer = 0
            self.frame_index += 1
            if self.frame_index >= len(self.animation_list[self.curr_animation]):
                self.frame_index = 0

    def render(self, screen):
        image = self.animation_list[self.curr_animation][self.frame_index]
        screen.blit(image, (self.x, self.y))

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def set_animation(self, animation_name):
        self.curr_animation = animation_name
        self.frame_index = 0

    def is_finished(self):
        return self.frame_index == len(self.animation_list[self.curr_animation]) - 1

    def set_animation_list(self, animation_list):
        self.animation_list = animation_list

    def set_frame_duration(self, frame_duration):
        self.frame_duration = frame_duration

    def set_frame_index(self, frame_index):
        self.frame_index = frame_index

    def set_frame_timer(self, frame_timer):
        self.frame_timer = frame_timer

    def set_curr_animation(self, curr_animation):
        self.curr_animation = curr_animation

    def get_position(self):
        return self.x, self.y

    def get_animation(self):
        return self.curr_animation

    def get_frame_index(self):
        return self.frame_index

    def get_frame_timer(self):
        return self.frame_timer

    def get_frame_duration(self):
        return self.frame_duration

    def get_animation_list(self):
        return self.animation_list