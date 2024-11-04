from enum import Enum
from src.Util import SpriteManager, DeckLoader
from src.StateMachine import StateMachine
from src.battleSystem.Buff import Buff
from src.battleSystem.battleEntity.Player import Player

g_state_manager = StateMachine()

sprite_collection = SpriteManager().spriteCollection

card_dict = sprite_collection["card"] # old version
CARD_DEFS = sprite_collection["card_conf"]  # dict { "name": CardConf class}

DECK_DEFS = DeckLoader().deck_conf  # dict {"name" : DeckConf class}
