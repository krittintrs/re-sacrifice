import pygame


class Buff():
    def __init__(self, name, duration, value, image):
        self.name = name
        self.duration = duration
        self.image = image
        self.value = value  # [1,0,0,0] == [atk,def,spd,range]

        self.x = 0
        self.y = 0
        self.rect = pygame.Rect(self.x, self.y, 20, 20)

        self.tooltipFlag = False

    def apply(self, entity):
        entity.attack += self.value[0]
        entity.defense += self.value[1]
        entity.speed += self.value[2]
        entity.range += self.value[3]

    def is_active(self):
        if self.duration == -1:  # -1 means infinite duration
            return True
        elif self.duration > 0:
            return True
        else:
            return False

    def next_turn(self):
        if self.duration > 0:
            self.duration -= 1

    def update(self, dt, events):
        self.rect.x = self.x
        self.rect.y = self.y
        
        mouse_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos):
            self.tooltipFlag = True
        else:
            self.tooltipFlag = False

    def render(self, screen):
        if self.tooltipFlag:
            font = pygame.font.Font(None, 24)
            tooltip_text = f"{self.name}: {self.value}"
            text_surface = font.render(tooltip_text, True, (0, 0, 0))
            text_rect = text_surface.get_rect()
            text_rect.topleft = (self.rect.x + 25, self.rect.y)
            screen.blit(text_surface, text_rect)
