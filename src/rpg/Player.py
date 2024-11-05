from src.rpg.EntityBase import EntityBase
from src.dependency import *
from src.StateMachine import StateMachine
class Player(EntityBase):
    def __init__(self, conf):
        super(Player, self).__init__(conf)

    def update(self, dt, events):
        super().update(dt, events)


    def Collides(self, target):
        y, height = self.y, self.height
        
        return not (self.x + self.width < target.x or self.x > target.x + target.width or
                    y + height + 10 < target.y or y+20 > target.y + target.height)


    def render(self, screen, adjacent_offset_x=0, adjacent_offset_y=0):
        # Adjust player's coordinates based on the camera offset
        render_x = self.x + adjacent_offset_x
        render_y = self.y + adjacent_offset_y
        
        # Handle invulnerability flashing effect
        if self.invulnerable and self.flash_timer > 0.06:
            self.flash_timer = 0
            if self.curr_animation.idleSprite is not None:
                self.curr_animation.idleSprite.set_alpha(64)
            self.curr_animation.image.set_alpha(64)

        # Render the player at the calculated coordinates
        if self.curr_animation and self.curr_animation.image:
            screen.blit(self.curr_animation.image, (render_x, render_y))
        
        # Reset alpha after flashing
        if self.invulnerable:
            if self.curr_animation.idleSprite is not None:
                self.curr_animation.idleSprite.set_alpha(255)
            self.curr_animation.image.set_alpha(255)

    def CreateAnimations(self):
        self.animation_list = gPlayer_animation_list