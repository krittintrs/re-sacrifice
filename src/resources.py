from enum import Enum
from src.Util import SpriteManager, DeckLoader
from src.StateMachine import StateMachine
from src.battleSystem.Buff import Buff
from src.battleSystem.battleEntity.Player import Player

g_state_manager = StateMachine()

sprite_collection = SpriteManager().spriteCollection

card_dict = sprite_collection["card"] # old version
CARD_DEFS = sprite_collection["card_conf"]# dict { "name": CardConf class}

DECK_DEFS = DeckLoader().deck_conf# dict {"name" : DeckConf class}

# for i in CARD_DEFS:
#     print(i, end=" : \n")
#     CARD_DEFS[i].display_attributes()
#     print("------------------")

# for i in DECK_DEFS:
#     print(i, end=" : \n")
#     print(DECK_DEFS[i].card_dict)


bonus_buff = [
    Buff('bonus_attack', 1, [1, 0, 0, 0]),
    Buff('bonus_defense', 1, [0, 1, 0, 0]),
    Buff('bonus_speed', 1, [0, 0, 1, 0])
]