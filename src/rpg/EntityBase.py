import pygame



class EntityBase():
    def __init__(self, conf):
        self.direction = 'down'
        self.animation_list = conf.animation

        # dims
        self.x = conf.x
        self.y = conf.y
        self.width = conf.width
        self.height = conf.height

        # sprite offset          check
        self.offset_x = conf.offset_x or 0
        self.offset_y = conf.offset_y or 0

        self.walk_speed = conf.walk_speed

        self.health = conf.health

        #invincible
        self.invulnerable = False
        self.invulnerable_duration = 0
        self.invulnerable_timer = 0

        #timer for turning transparency (flash)
        self.flash_timer = 0

        self.is_dead = False
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.state_machine = None
        self.curr_animation = None


    def CreateAnimations(self):
        pass

    def ChangeCoord(self, x=None, y=None):
        if x is not None:
            self.x = x
            self.rect.x = self.x

        if y is not None:
            self.y=y
            self.rect.y = self.y

    def MoveX(self, x):
        self.x += x
        self.rect.x = self.x

    def MoveY(self, y):
        self.y += y
        self.rect.y = self.y

    def Collides(self, target):
        return not(self.rect.x + self.width < target.rect.x or self.rect.x > target.rect.x + target.width or
                   self.rect.y + self.height < target.rect.y or self.rect.y > target.rect.y + target.height)

    def Damage(self, dmg):
        self.health -= dmg

    def SetInvulnerable(self, duration):
        self.invulnerable = True
        self.invulnerable_duration = duration

    def ChangeState(self, name):
        self.state_machine.Change(name)

    def ChangeAnimation(self, name):
        self.curr_animation = self.animation_list[name]

    def update(self, dt, events):

        self.state_machine.update(dt, events)

        if self.curr_animation:
            self.curr_animation.update(dt)

    def ProcessAI(self, params, dt):
        self.state_machine.ProcessAI(params, dt)

    def render(self, adjacent_offset_x=0, adjacent_offset_y=0):
        if self.invulnerable and self.flash_timer > 0.06:
            self.flash_timer = 0
            if self.curr_animation.idleSprite is not None:
                self.curr_animation.idleSprite.set_alpha(64)
            self.curr_animation.image.set_alpha(64)

        self.x = self.x + adjacent_offset_x
        self.y = self.y + adjacent_offset_y
        self.state_machine.render()
        if self.curr_animation.idleSprite is not None:
            self.curr_animation.idleSprite.set_alpha(255)
        self.curr_animation.image.set_alpha(255)

        self.x = self.x - adjacent_offset_x
        self.y = self.y - adjacent_offset_y

