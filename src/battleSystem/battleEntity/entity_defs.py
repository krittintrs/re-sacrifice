from src.dependency import *

class PlayerConf:
    def __init__(self, name, job, deckInv):
        self.name = name
        self.job = job
        self.deckInv = deckInv

class EnemyConf:
    def __init__(self, name, animationList, deckInv):
        self.name = name
        self.animationList = animationList
        self.deckInv = deckInv

BATTLE_ENTITY = {
    "default_warrior": PlayerConf("player", PlayerClass.WARRIOR, DECK_DEFS["default"]),
    "default_ranger": PlayerConf("player", PlayerClass.RANGER, DECK_DEFS["default"]),
    "default_mage": PlayerConf("player", PlayerClass.MAGE, DECK_DEFS["default"]),
    "default_enemy": EnemyConf("enemy", gNormalGoblin_animation_list, DECK_DEFS["default"])
}

