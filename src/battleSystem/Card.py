import pygame
from src.dependency import *

class Card:
    def __init__(self, id=None, name=None, class_=None, type=None, description=None, image=None, attack=None, defense=None, speed=None, range_start=None, range_end=None, beforeEffect = [], mainEffect = [], afterEffect = []):
        # For Render
        self.id = id
        self.class_ = class_
        self.type = type
        self.vfxType = None
        self.animationType = None
        self.name = name
        self.description = description
        self.image = image
        self.isSelected = False

        # Card Stats
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.range_start = range_start
        self.range_end = range_end

        # Card Buffed Stats
        self.buffed_attack = attack
        self.buffed_defense = defense
        self.buffed_speed = speed
        self.buffed_range_start = range_start
        self.buffed_range_end = range_end

        # Card Effects
        self.beforeEffect = beforeEffect # list of Effects
        self.mainEffect = mainEffect
        self.afterEffect = afterEffect

    def read_conf(self, conf):
        # For Render
        self.id = conf.id
        self.class_ = conf.class_
        self.type = conf.type
        self.vfxType = conf.vfx_type
        self.animationType = conf.animation_type
        self.name = conf.name
        self.description = conf.description
        self.image = conf.image
        self.isSelected = False

        # Card Stats
        self.attack = conf.attack
        self.defense = conf.defense
        self.speed = conf.speed
        self.range_start = conf.range_start
        self.range_end = conf.range_end

        # Card Effects
        self.beforeEffect = getattr(conf, "beforeEffect", [])
        self.mainEffect = getattr(conf, "mainEffect", [])
        self.afterEffect = getattr(conf, "afterEffect", [])

    def print_stats(self):
        print(f'{self.name} stats - ATK: {self.attack}, DEF: {self.defense}, SPD: {self.speed}, RNG: {self.range_start}-{self.range_end}')

    def print_effects(self):
        print(f'{self.name} effects')
        print('Before Effects:')
        for effect in self.beforeEffect:
            print(effect.type)
        print('Main Effects:')
        for effect in self.mainEffect:
            print(effect.type)
        print('After Effects:')
        for effect in self.afterEffect:
            print(effect.type)
        print('>>>>>>>>><<<<<<<<<<')

    def reset_stats(self):
        self.buffed_attack = self.attack
        self.buffed_defense = self.defense
        self.buffed_speed = self.speed
        self.buffed_range_start = self.range_start
        self.buffed_range_end = self.range_end

    def start(self, entity, enemy, field):
        # Perform card action
        pass

    def before(self, entity, enemy, field):
        # Perform card action before the main action
        pass

    def damage(self, entity, enemy, field):
        # Perform card action for damage
        pass

    def end(self, entity, enemy, field):
        # Perform card action at the end
        pass

    def render(self, screen, order):
        # Transparent card rendering at the bottom
        start_x = 80 + order * (CARD_WIDTH + 30)  # Space cards with 30px gap
        start_y = SCREEN_HEIGHT - HUD_HEIGHT//2 - CARD_HEIGHT//2  # Place near the bottom

        # Draw the card image
        screen.blit(self.image, (start_x, start_y))

        # Draw card modified numbers
        normal_color = (0, 0, 0)
        buff_color = (0, 167, 0)
        debuff_color = (230, 0, 0)
        
        # Draw the speed value
        if self.buffed_speed > self.speed:
            color = buff_color
        elif self.buffed_speed < self.speed:
            color = debuff_color
        else:
            color = normal_color
        font = gFont_list["default"]
        text = font.render(f'{self.buffed_speed}', True, color)
        screen.blit(text, (start_x + 171, start_y + 15))

        # Draw the attack value
        if self.buffed_attack > self.attack:
            color = buff_color
        elif self.buffed_attack < self.attack:
            color = debuff_color
        else:
            color = normal_color
        font = gFont_list["default"]
        text = font.render(f'{self.buffed_attack}', True, color)
        screen.blit(text, (start_x + 45, start_y + 212))

        # Draw the range value
        if self.buffed_range_end > self.range_end:
            color = buff_color
        elif self.buffed_range_end < self.range_end:
            color = debuff_color
        else:
            color = normal_color
        if self.range_start == self.range_end:
            font2 = gFont_list["default"]
            text = font2.render(f'{self.buffed_range_end}', True, color)
            screen.blit(text, (start_x + 96, start_y + 212))
        else:
            font2 = gFont_list["small"]
            text = font2.render(f'{self.buffed_range_start}-{self.buffed_range_end}', True, color)
            screen.blit(text, (start_x + 91, start_y + 213))

        # Draw the defense value
        if self.buffed_defense > self.defense:
            color = buff_color
        elif self.buffed_defense < self.defense:
            color = debuff_color
        else:
            color = normal_color
        text = font.render(f'{self.buffed_defense}', True, color)
        screen.blit(text, (start_x + 146, start_y + 212))

        # if selected
        if self.isSelected:
            # Highlight the selected card by rendering a thicker border
            pygame.draw.rect(screen, (255, 255, 0), (start_x, start_y, CARD_WIDTH, CARD_HEIGHT), 3)

    # def render_selected(self, screen, selected_index):
    #     # Highlight the selected card by rendering a thicker border
    #     start_x = 80 + selected_index * (CARD_WIDTH + 30)
    #     start_y = SCREEN_HEIGHT - CARD_HEIGHT - 10
        
    #     # Draw the highlighted border around the card
    #     pygame.draw.rect(screen, (255, 255, 0), (start_x, start_y, CARD_WIDTH, CARD_HEIGHT), 3)

    def update(self, dt, events):
        pass
