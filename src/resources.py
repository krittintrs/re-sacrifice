from src.Util import SpriteManager, DeckLoader
from src.StateMachine import StateMachine
from src.EnumResources import *
import pygame

g_state_manager = StateMachine()

sprite_collection = SpriteManager().spriteCollection

CARD_DEFS = sprite_collection["card_conf"]  # dict {"name": CardConf class}
DECK_DEFS = DeckLoader().deck_conf          # dict {"name": DeckConf class}

gSounds = {
    "dice_roll": pygame.mixer.Sound("sounds/dice_roll.mp3"),
    "attack": pygame.mixer.Sound("sounds/attack.wav"),
    "block": pygame.mixer.Sound("sounds/block.wav"),
}

gBuffIcon_image_list = {
    "buff": sprite_collection["buff_icon"].image,
    "debuff": sprite_collection["debuff_icon"].image,
    "attack": sprite_collection["attack_icon"].image,
    "defense": sprite_collection["defense_icon"].image,
    "speed": sprite_collection["speed_icon"].image,
    "range": sprite_collection["range_icon"].image,
    "critical": sprite_collection["critical_icon"].image,
    "cant_move": sprite_collection["cant_move_icon"].image,
    "fire": sprite_collection["fire_icon"].image,
}

gWarrior_animation_list = {
    "cast": sprite_collection["cast_warrior"].animation,
    "cast_loop": sprite_collection["castloop_warrior"].animation,
    "multi_attack": sprite_collection["multiAttack_warrior"].animation,
    "single_attack": sprite_collection["singleAttack_warrior"].animation,
    "idle": sprite_collection["idle_warrior"].animation,
    "knock_down": sprite_collection["knockDown_warrior"].animation,
    "walk": sprite_collection["walk_warrior"].animation,
}

gRanger_animation_list = {
    "cast": sprite_collection["cast_ranger"].animation,
    "cast_loop": sprite_collection["castloop_ranger"].animation,
    "multi_attack": sprite_collection["multiAttack_ranger"].animation,
    "single_attack": sprite_collection["singleAttack_ranger"].animation,
    "idle": sprite_collection["idle_ranger"].animation,
    "knock_down": sprite_collection["knockDown_ranger"].animation,
    "walk": sprite_collection["walk_ranger"].animation,
}

gMage_animation_list = {
    "cast": sprite_collection["cast_mage"].animation,
    "cast_loop": sprite_collection["castloop_mage"].animation,
    "multi_attack": sprite_collection["multiAttack_mage"].animation,
    "single_attack": sprite_collection["singleAttack_mage"].animation,
    "idle": sprite_collection["idle_mage"].animation,
    "knock_down": sprite_collection["knockDown_mage"].animation,
    "walk": sprite_collection["walk_mage"].animation,
}

gNormalGoblin_animation_list = {
    "idle": sprite_collection["normalGoblinIdle"].animation,
    "attack": sprite_collection["normalGoblinAttack"].animation,
    "death": sprite_collection["normalGoblinDeath"].animation,
    "walk": sprite_collection["normalGoblinWalk"].animation,
}

gGhost_animation_list = {
    "idle": sprite_collection["ghostIdle"].animation,
    "attack": sprite_collection["ghostAttack"].animation,
    "death": sprite_collection["ghostDeath"].animation,
    "summon": sprite_collection["ghostSummon"].animation,
}

gTrap_animation_list = {
    "idle": sprite_collection["trapIdle"].animation,
    "attack": sprite_collection["trapAttack"].animation,
    "summon":sprite_collection["trapSummon"].animation,
    "death":sprite_collection["trapDeath"].animation,
}

gEntity_animation_dict = {
    "warrior": gWarrior_animation_list,
    "ranger": gRanger_animation_list,
    "mage": gMage_animation_list,
    "goblin": gNormalGoblin_animation_list,
    "ghost":gGhost_animation_list,
    "trap":gTrap_animation_list
}

gBackground_image_list = {
    BackgroundState.BATTLE: pygame.image.load("./graphics/battle_background.png"), 
    BackgroundState.DECK_BUILDING: pygame.image.load("./graphics/deckbuilding_background.png"),
}

gClock_image_list = {
    "clock_0": sprite_collection["clock_0"].image,
    "clock_3": sprite_collection["clock_3"].image,
    "clock_6": sprite_collection["clock_6"].image,
    "clock_9": sprite_collection["clock_9"].image,
}

gDice_image_list = {
    "dice_1": sprite_collection["dice_1"].image,
    "dice_2": sprite_collection["dice_2"].image,
    "dice_3": sprite_collection["dice_3"].image,
    "dice_4": sprite_collection["dice_4"].image,
    "dice_5": sprite_collection["dice_5"].image,
    "dice_6": sprite_collection["dice_6"].image,
    "dice_roll_1": sprite_collection["dice_roll_1"].image,
    "dice_roll_2": sprite_collection["dice_roll_2"].image,
    "dice_roll_3": sprite_collection["dice_roll_3"].image,
    "dice_roll_4": sprite_collection["dice_roll_4"].image,
    "dice_roll_5": sprite_collection["dice_roll_5"].image,
    "dice_roll_6": sprite_collection["dice_roll_6"].image,
}

gField_image_list = {
    "normal": sprite_collection["field_normal"].image,
    "player_available": sprite_collection["field_player_available"].image,
    "player_current": sprite_collection["field_player_current"].image,
    "enemy_available": sprite_collection["field_enemy_available"].image,
    "enemy_current": sprite_collection["field_enemy_current"].image,
}

gFont_list = {
    "small": pygame.font.Font("./fonts/Minecraftia-Regular.ttf", 8),
    "default": pygame.font.Font("./fonts/Minecraftia-Regular.ttf", 10),
    "header": pygame.font.Font("./fonts/Minecraftia-Regular.ttf", 15),
    "title": pygame.font.Font("./fonts/Minecraftia-Regular.ttf", 20),
}

gVfx_animation_list = {
    "mage_heavy_vfx": sprite_collection["mage_heavy_vfx"].animation,
    "mage_light_vfx": sprite_collection["mage_light_vfx"].animation,
    "mage_debuff_vfx": sprite_collection["mage_debuff_vfx"].animation,
    "mage_explosion_vfx": sprite_collection["mage_explosion_vfx"].animation,
    "mage_true_vfx": sprite_collection["mage_true_vfx"].animation,
    "ranger_heavy_vfx": sprite_collection["ranger_heavy_vfx"].animation,
    "ranger_light_vfx": sprite_collection["ranger_light_vfx"].animation,
    "ranger_shot_vfx": sprite_collection["ranger_shot_vfx"].animation,
    "warrior_heavy_vfx": sprite_collection["warrior_heavy_vfx"].animation,
    "warrior_light_vfx": sprite_collection["warrior_light_vfx"].animation,
    "warrior_blood_vfx": sprite_collection["warrior_blood_vfx"].animation,
    "warrior_strike_vfx": sprite_collection["warrior_strike_vfx"].animation,
    "monster_attack_vfx": sprite_collection["monster_attack_vfx"].animation,
    "buff_vfx": sprite_collection["buff_vfx"].animation,
    "debuff_vfx": sprite_collection["debuff_vfx"].animation,
    "dizzy_vfx": sprite_collection["dizzy_vfx"].animation,
    "firefly_vfx": sprite_collection["firefly_vfx"].animation,
    "leavesFalling_vfx": sprite_collection["leavesFalling_vfx"].animation,
    "magicHit_vfx": sprite_collection["magicHit_vfx"].animation,
    "physicalHit_vfx": sprite_collection["physicalHit_vfx"].animation,
    "shield_vfx": sprite_collection["shield_vfx"].animation,
}