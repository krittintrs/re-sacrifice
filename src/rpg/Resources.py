import pygame
from src.rpg.Utils import SpriteManager, Animation
import src.rpg.Utils as Util
from src.rpg.StateMachine import *

g_state_manager = StateMachine()

sprite_collection = SpriteManager().spriteCollection


gPlayer_animation_list = {"down": sprite_collection["character_walk_down"].animation,
                         "right": sprite_collection["character_walk_right"].animation,
                         "up": sprite_collection["character_walk_up"].animation,
                         "left": sprite_collection["character_walk_left"].animation
}

ITEM_DESCRIPTIONS = {
    "Health Potion": "A potion that restores 50 HP.",
    "Mana Potion": "A potion that restores 30 MP.",
    "Key": "A mysterious key that might unlock something important.",
    "Gold": "Money",
    "Amulet": "A mysterious amulet"
}

# gFonts = {
#     'small': pygame.font.Font('fonts/font.ttf', 24),
#     'medium': pygame.font.Font('fonts/font.ttf', 48),
#     'large': pygame.font.Font('fonts/font.ttf', 96),
#     'zelda_small': pygame.font.Font('fonts/zelda.otf', 96),
#     'zelda': pygame.font.Font('fonts/zelda.otf', 192),
#     'gothic_medium': pygame.font.Font('fonts/GothicPixels.ttf', 48),
#     'gothic_large': pygame.font.Font('fonts/GothicPixels.ttf', 96),

# }