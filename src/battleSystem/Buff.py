import pygame
from src.dependency import *

class Buff():
    def __init__(self, conf):
        self.name = conf.name
        self.description = conf.description
        self.duration = conf.duration
        self.type = conf.type
        self.value = conf.value  # [1,0,0,0] == [atk,def,spd,range]
        self.dot_damage = conf.dot_damage
        self.imageName = conf.imageName

        self.x = 0
        self.y = 0
        self.rect = pygame.Rect(self.x, self.y, 20, 20)

        self.tooltipFlag = False

    def print(self):
        print(f'{self.name}: {self.value} / {self.duration}')

    def apply(self, card):
        card.buffed_attack += self.value[0]
        card.buffed_defense += self.value[1]
        card.buffed_speed += self.value[2]
        card.buffed_range_end += self.value[3]

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
        if self.imageName is not None:
            self.y = 100
            screen.blit(self.imageName, (self.x, 100))

            # Render buff or debuff icon border
            if self.type == BuffType.BUFF:
                screen.blit(gBuffIcon_image_list["buff"], (self.x + 10, 110))
            elif self.type == BuffType.DEBUFF:
                screen.blit(gBuffIcon_image_list["debuff"], (self.x + 10, 110))
            elif self.type == BuffType.DICE_ROLL:
                dice_roll_icon = pygame.font.SysFont("Sans Serif", 20).render("B", True, (0, 0, 0))
                screen.blit(dice_roll_icon, (self.x + 10, 110))
            elif self.type == BuffType.PERM_BUFF:
                perm_buff_icon = pygame.font.SysFont("Sans Serif", 20).render("P", True, (0, 0, 0))
                screen.blit(perm_buff_icon, (self.x + 10, 110))
            elif self.type == BuffType.EMPOWER:
                screen.blit(gBuffIcon_image_list["attack"], (self.x, 100))
                screen.blit(gBuffIcon_image_list["buff"], (self.x + 10, 110))
            elif self.type == BuffType.BLOOD:
                flipped_attack_icon = pygame.transform.flip(gBuffIcon_image_list["attack"], True, False)
                screen.blit(flipped_attack_icon, (self.x, 100))
                blood_icon = pygame.font.SysFont("Sans Serif", 20).render("B", True, (255, 0, 0))
                screen.blit(blood_icon, (self.x + 10, 110))
            elif self.type == BuffType.CRIT_RATE:
                crit_rate_icon = pygame.font.SysFont("Sans Serif", 20).render("R", True, (0, 0, 0))
                screen.blit(crit_rate_icon, (self.x + 10, 110))
            elif self.type == BuffType.CRIT_DMG:
                crit_dmg_icon = pygame.font.SysFont("Sans Serif", 20).render("D", True, (0, 0, 0))
                screen.blit(crit_dmg_icon, (self.x + 10, 110))


            # try to render buff icon border
            # pygame.draw.rect(screen, (0, 0, 0), (buff_x_position, buff.y, buff.rect.width, buff.rect.height), 1)

        if self.tooltipFlag:
            font = pygame.font.SysFont("Arial", 20)  # Smaller size for slimmer appearance
            if self.duration == -1:
                tooltip_text = f"Gain {self.description} permanently"
            else:
                if self.duration > 1:
                    tooltip_text = f"{self.description} for {self.duration} turns"
                else:
                    tooltip_text = f"{self.description} for {self.duration} turn"
                        
            # Render buff name
            buff_name_surface = font.render(self.name, True, (0, 0, 0))
            buff_name_rect = buff_name_surface.get_rect()
            buff_name_rect.topleft = (self.rect.x + 25, self.rect.y - 40)
            screen.blit(buff_name_surface, buff_name_rect)
            
            # Use a lighter gray color to make the font look less strong
            text_surface = font.render(tooltip_text, True, (140, 140, 140)) 
            text_rect = text_surface.get_rect()
            text_rect.topleft = (self.rect.x + 25, self.rect.y - 20)
            screen.blit(text_surface, text_rect)