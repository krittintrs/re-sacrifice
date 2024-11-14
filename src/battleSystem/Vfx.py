from src.dependency import *


class Vfx:
    def __init__(self, animation_list, x, y, entity):
        self.animation_list = animation_list
        self.curr_animation = None
        self.finish = True
        self.x = x
        self.y = y
        self.animation_order = []
        self.vfxAnimation = None
        self.entity = entity
        self.stunted = False

    def update(self, dt, x, y):
        self.x = x 
        self.y = y

        if self.curr_animation is not None and not self.finish:
            if self.curr_animation in self.animation_list:
                if self.curr_animation == "dizzy_vfx" and not self.stunted:
                    self.entity.ChangeAnimation("stunt")
                    self.stunted = True
                self.vfxAnimation = self.animation_list[self.curr_animation]
                if self.vfxAnimation is not None and self.vfxAnimation.finished:
                    self.vfxAnimation.finished = False
                    self.vfxAnimation.index = 0
                    if self.vfxAnimation.times_played > 0:
                        self.vfxAnimation.times_played = 0
                self.vfxAnimation.update(dt)
                if self.vfxAnimation.is_finished():
                    self.finish = True
                    if len(self.animation_order) == 0:
                        self.curr_animation = None        
        else:
            if len(self.animation_order) != 0 and self.finish:
                self.curr_animation = self.animation_order.pop(0)
                self.finish = False

    def render(self, screen):
        if self.curr_animation is not None:
            if self.animation_list and self.curr_animation in self.animation_list:
                self.vfxAnimation = self.animation_list[self.curr_animation]
                self.vfxAnimation.render(screen, self.x + self.offset_x + self.vfxAnimation.offset_x, self.y + self.offset_y + self.vfxAnimation.offset_y)


    def play(self, name, offset_x=-20, offset_y=0):
        # Check if name is an instance of VFXType
        if isinstance(name, VFXType):
            vfx_name = name.value  # Access the value if it's an enum
        else:
            vfx_name = name  # Use directly if it's already a string

        print(f"Vfx play: {vfx_name}")
        self.animation_order.append(vfx_name)
        self.stunted = False
        self.offset_x = offset_x
        self.offset_y = offset_y
        print(f"Vfx play: {name} animation_order: {self.animation_order}")

    def stop(self):
        if self.vfxAnimation is not None:
            print(f"Vfx stop: {self.vfxAnimation.name}")
            if self.vfxAnimation.looping:
                self.curr_animation = None
                self.vfxAnimation.stop()
                self.finish = True
            else:
                print(f"{self.vfxAnimation.name}: animation is not looping")

