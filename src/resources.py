from src.Util import SpriteManager, DeckLoader
from src.StateMachine import StateMachine
import pygame

g_state_manager = StateMachine()

sprite_collection = SpriteManager().spriteCollection

CARD_DEFS = sprite_collection["card_conf"]  # dict {"name": CardConf class}
DECK_DEFS = DeckLoader().deck_conf          # dict {"name": DeckConf class}

gBuffIcon_image_list = {"buff": sprite_collection["buff_icon"], "debuff": sprite_collection["debuff_icon"], "attack": sprite_collection["attack_icon"],
                 "defense": sprite_collection["defense_icon"], "speed": sprite_collection["speed_icon"], "range": sprite_collection["range_icon"]}

gSounds = {
    'dice_roll': pygame.mixer.Sound("sounds/dice_roll.mp3"),
    'attack': pygame.mixer.Sound("sounds/attack.wav"),
    'block': pygame.mixer.Sound("sounds/block.wav"),
}

gBuffIcon_image_list = {"buff": sprite_collection["buff_icon"].image,
                        "debuff": sprite_collection["debuff_icon"].image,
                        "attack": sprite_collection["attack_icon"].image,
                        "defense": sprite_collection["defense_icon"].image,
                        "speed": sprite_collection["speed_icon"].image,
                        "range": sprite_collection["range_icon"].image}

gWarrior_animation_list = {
    "cast": sprite_collection["cast_warrior"].animation,
    "cast_loop": sprite_collection["castloop_warrior"].animation,
    "multi_attack": sprite_collection["multiAttack_warrior"].animation,
    "single_attack": sprite_collection["singleAttack_warrior"].animation,
    "idle": sprite_collection["idle_warrior"].animation,
    "knock_down": sprite_collection["knockDown_warrior"].animation,
    "walk": sprite_collection["walk_warrior"].animation
}

gRanger_animation_list = {
    "cast": sprite_collection["cast_ranger"].animation,
    "cast_loop": sprite_collection["castloop_ranger"].animation,
    "multi_attack": sprite_collection["multiAttack_ranger"].animation,
    "single_attack": sprite_collection["singleAttack_ranger"].animation,
    "idle": sprite_collection["idle_ranger"].animation,
    "knock_down": sprite_collection["knockDown_ranger"].animation,
    "walk": sprite_collection["walk_ranger"].animation
}

gMage_animation_list = {
    "cast": sprite_collection["cast_mage"].animation,
    "cast_loop": sprite_collection["castloop_mage"].animation,
    "multi_attack": sprite_collection["multiAttack_mage"].animation,
    "single_attack": sprite_collection["singleAttack_mage"].animation,
    "idle": sprite_collection["idle_mage"].animation,
    "knock_down": sprite_collection["knockDown_mage"].animation,
    "walk": sprite_collection["walk_mage"].animation
}

gNormalGoblin_animation_list = {
    "idle": sprite_collection["normalGoblinIdle"].animation,
    "attack": sprite_collection["normalGoblinAttack"].animation,
    "death": sprite_collection["normalGoblinDeath"].animation,
    "walk": sprite_collection["normalGoblinWalk"].animation
}