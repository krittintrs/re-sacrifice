import pygame
from src.dependency import *
from src.battleSystem.Deck import Deck
import tween


class SubEntityConf:
    def __init__(self, name, animation_list=None, health=10, is_occupied_field = False, attack = 1, duration = -1, range = 1):
        self.name = name
        self.animation_list = animation_list
        self.is_occupied_field = is_occupied_field
        self.health = health
        self.attack = attack
        self.duration = duration
        self.range = range


SUB_ENTITY = {
    "trap" : SubEntityConf("trap", gEntity_animation_dict["goblin"], 1, False, 0, 2, 0), # please find some animation for the trap replace goblin for me please.
    "pheonix": SubEntityConf("pheonix", gEntity_animation_dict["goblin"], 4, False, 1, 5, 2)
}

