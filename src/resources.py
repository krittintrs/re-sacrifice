from enum import Enum
from src.Util import SpriteManager, DeckLoader
from src.StateMachine import StateMachine
from src.battleSystem.Buff import Buff
from src.battleSystem.battleEntity.Player import Player

g_state_manager = StateMachine()

sprite_collection = SpriteManager().spriteCollection

card_dict = sprite_collection["card"]

dect_dict = DeckLoader(card_dict).deck_dict

default_deck = dect_dict["default"]
default_player = Player("player")
default_player.deck = default_deck

bonus_buff = [
    Buff('bonus_attack', 1, [1, 0, 0, 0]),
    Buff('bonus_defense', 1, [0, 1, 0, 0]),
    Buff('bonus_speed', 1, [0, 0, 1, 0])
]

class BattleState(Enum):
    DECK_BUILDING = "deckBuilding"
    PREPARATION_PHASE = "battlePrepare"
    INITIAL_PHASE = "battleInitial"
    SELECTION_PHASE = "battleSelect"
    ACTION_PHASE = "battleAction"
    RESOLVE_PHASE = "battleResolve"
    END_PHASE = "battleEnd"
    FINISH_PHASE = "battleFinish"

class SelectionState(Enum):
    ATTACK = "attack"
    MOVE = "move"
    BUFF = "buff"

class PlayerType(Enum):
    PLAYER = 1
    ENEMY = 2

class EffectType(Enum):
    ATTACK = "attack"
    MOVE = "move"
    SELF_BUFF = "self_buff"
    RANGE_BUFF = "range_buff"
    PUSH = "push"
    PULL = "pull"
    DEBUFF = "debuff"
    BUFF = "buff"
    CLEANSE = "cleanse"
    SAND_THROW = "SandThrow"
    ANGEL_BLESSING = "AngelBlessing"
    DESTINY_DRAW = "DestinyDraw"
    RESET = "Reset"
    KAMIKAZE = "Kamikaze"
    SPAWN = "spawn"
    HEAL = "heal"
    DITTO = "ditto"
    BLOOD_SACRIFICE = "bloodSacrifice"
    DISCARD = "discard"

class CardType(Enum):
    MOVE = "Move"
    ATTACK = "Attack"
    DEFENSE = "Defense"
    BUFF = "Buff"
    DEBUFF = "Debuff"
    SPECIAL = "Special"


class CardClass(Enum):
    COMMON = "Common"
    GK_NOW = "GK Now"
    GK_PAST = "GK Past"
    RH_MAN = "RH Man"
    WARRIOR = "Warrior"
    RANGER = "Ranger"
    MAGE = "Mage"