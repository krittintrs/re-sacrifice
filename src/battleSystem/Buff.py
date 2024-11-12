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
        self.y = BUFF_Y
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
            screen.blit(self.imageName, (self.x, self.y))

            # Render buff or debuff icon border
            if self.type == BuffType.BUFF:
                screen.blit(gBuffIcon_image_list["buff"], (self.x + 10, self.y + 10))
            elif self.type == BuffType.DEBUFF:
                screen.blit(gBuffIcon_image_list["debuff"], (self.x + 10, self.y + 10))
            elif self.type == BuffType.DICE_ROLL:
                dice_roll_icon = pygame.font.SysFont("Sans Serif", 20).render("B", True, (0, 0, 0))
                screen.blit(dice_roll_icon, (self.x + 10, self.y + 10))
            elif self.type == BuffType.PERM_BUFF:
                perm_buff_icon = pygame.font.SysFont("Sans Serif", 20).render("P", True, (0, 0, 0))
                screen.blit(perm_buff_icon, (self.x + 10, self.y + 10))
            elif self.type == BuffType.EMPOWER:
                screen.blit(gBuffIcon_image_list["attack"], (self.x, self.y))
                screen.blit(gBuffIcon_image_list["buff"], (self.x + 10, self.y + 10))
            elif self.type == BuffType.BLOOD:
                flipped_attack_icon = pygame.transform.flip(gBuffIcon_image_list["attack"], True, False)
                screen.blit(flipped_attack_icon, (self.x, self.y))
                blood_icon = pygame.font.SysFont("Sans Serif", 20).render("B", True, (255, 0, 0))
                screen.blit(blood_icon, (self.x + 10, self.y + 10))
            elif self.type == BuffType.CRIT_RATE:
                crit_rate_icon = pygame.font.SysFont("Sans Serif", 20).render("R", True, (0, 0, 0))
                screen.blit(crit_rate_icon, (self.x + 10, self.y + 10))
            elif self.type == BuffType.CRIT_DMG:
                crit_dmg_icon = pygame.font.SysFont("Sans Serif", 20).render("D", True, (0, 0, 0))
                screen.blit(crit_dmg_icon, (self.x + 10, self.y + 10))

            # try to render buff icon border
            # pygame.draw.rect(screen, (0, 0, 0), (buff_x_position, buff.y, buff.rect.width, buff.rect.height), 1)

        if self.tooltipFlag:
            font = gFont_list["default"]  # Smaller size for slimmer appearance

            # Determine the tooltip text based on duration
            if self.duration == -1:
                tooltip_text = f"Gain {self.description} permanently"
            else:
                tooltip_text = f"{self.description} for {self.duration} turn{'s' if self.duration > 1 else ''}"

            # Render buff name
            buff_name_surface = font.render(self.name, True, (0, 0, 0))
            buff_name_rect = buff_name_surface.get_rect()
            buff_name_rect.topleft = (self.rect.x + 25, self.rect.y - 40)

            # Render tooltip text
            text_surface = font.render(tooltip_text, True, (255, 255, 255))
            text_rect = text_surface.get_rect()
            text_rect.topleft = (self.rect.x + 25, self.rect.y - 25)

            # Calculate background rectangle size
            padding = 5  # Add some padding around the text
            bg_rect_width = max(buff_name_rect.width, text_rect.width) + 2 * padding
            bg_rect_height = buff_name_rect.height + text_rect.height + padding
            bg_rect = pygame.Rect(buff_name_rect.left - padding, buff_name_rect.top - padding, bg_rect_width, bg_rect_height)

            # Draw background rectangle (use a light color)
            pygame.draw.rect(screen, (211, 164, 117), bg_rect, border_radius=5)  # border_radius makes the corners rounded

            # Draw border for the rectangle (optional)
            outer_border = pygame.Rect(buff_name_rect.left - padding - 2, buff_name_rect.top - padding - 2, bg_rect_width + 4, bg_rect_height + 4)
            middle_border = pygame.Rect(buff_name_rect.left - padding - 1, buff_name_rect.top - padding - 1, bg_rect_width + 2, bg_rect_height + 2)
            pygame.draw.rect(screen, (98, 65, 48), outer_border, width=2, border_radius=5)
            pygame.draw.rect(screen, (117, 85, 70), middle_border, width=2, border_radius=5)
            pygame.draw.rect(screen, (98, 65, 48), bg_rect, width=2, border_radius=5)

            # Blit the text on top of the background
            screen.blit(buff_name_surface, buff_name_rect)
            screen.blit(text_surface, text_rect)

            # pygame.draw.rect(screen, (255,0,0), buff_name_rect, 1)
            # pygame.draw.rect(screen, (0,255,0), text_rect, 1)