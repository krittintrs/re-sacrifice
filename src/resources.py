from src.Util import SpriteManager, DeckLoader
from src.StateMachine import StateMachine

g_state_manager = StateMachine()

sprite_collection = SpriteManager().spriteCollection

card_dict = sprite_collection["card"]  # old version
CARD_DEFS = sprite_collection["card_conf"]  # dict { "name": CardConf class}

DECK_DEFS = DeckLoader().deck_conf  # dict {"name" : DeckConf class}

gBuffIcon_image_list = {"buff": sprite_collection["buff_icon"].image, "debuff": sprite_collection["debuff_icon"].image, "attack": sprite_collection["attack_icon"].image,
                 "defense": sprite_collection["defense_icon"].image, "speed": sprite_collection["speed_icon"].image, "range": sprite_collection["range_icon"].image}

