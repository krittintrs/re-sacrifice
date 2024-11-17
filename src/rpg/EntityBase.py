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

    def ChangeState(self, name):
        self.state_machine.Change(name)

    def ChangeAnimation(self, name):
        self.curr_animation = self.animation_list[name]

    def update(self, dt, events):

        self.state_machine.update(dt, events)

        # if self.curr_animation:
        #     self.curr_animation.update(dt)

        # Check if an animation is set and update it
        if self.curr_animation:
            self.curr_animation.update(dt) 

    def ProcessAI(self, params, dt):
        self.state_machine.ProcessAI(params, dt)

    def render(self, screen, adjacent_offset_x=0, adjacent_offset_y=0):
        self.state_machine.render()


