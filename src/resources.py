from src.Util import SpriteManager, DeckLoader
from src.StateMachine import StateMachine
import pygame

g_state_manager = StateMachine()

sprite_collection = SpriteManager().spriteCollection

card_dict = sprite_collection["card"]  # old version
CARD_DEFS = sprite_collection["card_conf"]  # dict { "name": CardConf class}

DECK_DEFS = DeckLoader().deck_conf  # dict {"name" : DeckConf class}

gBuffIcon_image_list = {"buff": sprite_collection["buff_icon"], "debuff": sprite_collection["debuff_icon"], "attack": sprite_collection["attack_icon"],
                 "defense": sprite_collection["defense_icon"], "speed": sprite_collection["speed_icon"], "range": sprite_collection["range_icon"]}

gSounds = {
    'dice_roll': pygame.mixer.Sound("sounds/dice_roll.mp3"),
    'attack': pygame.mixer.Sound("sounds/attack.wav"),
    'block': pygame.mixer.Sound("sounds/block.wav"),
}