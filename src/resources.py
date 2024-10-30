from src.Util import SpriteManager
from src.StateMachine import StateMachine
from src.battleSystem.Buff import Buff

g_state_manager = StateMachine()

sprite_collection = SpriteManager().spriteCollection

card_dict = sprite_collection["card"]

bonus_buff = [
    Buff('bonus_attack', 1, [1, 0, 0, 0]),
    Buff('bonus_defense', 1, [0, 1, 0, 0]),
    Buff('bonus_speed', 1, [0, 0, 1, 0])
]