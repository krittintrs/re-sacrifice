from enum import Enum

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
    ATTACK = "SelectAttackState"
    MOVE = "SelectMoveState"
    BUFF = "SelectBuffState"
    PUSH = "SelectPushState"
    PULL = "SelectPullState"
    SPAWN = "SelectSpawnState"

class RPGState(Enum):
    START = "start"
    INTRO = "intro"
    TOWN = "town"
    TAVERN = "tavern"

class PlayerType(Enum):
    PLAYER = "player"
    ENEMY = "enemy"

class PlayerClass(Enum):
    WARRIOR = "Warrior"
    RANGER = "Ranger"
    MAGE = "Mage"

class EffectType(Enum):
    ATTACK = "attack"
    MOVE = "move"
    SELF_BUFF = "self_buff"
    OPPO_BUFF = "oppo_buff"
    ATTACK_SELF_BUFF = "attack_self_buff"
    ATTACK_OPPO_BUFF = "attack_oppo_buff"
    PUSH = "push"
    PULL = "pull"
    CLEANSE = "cleanse"
    DISCARD = "discard"
    SAND_THROW = "sand_throw"
    ANGEL_BLESSING = "angle_blessing"
    DESTINY_DRAW = "destiny_draw"
    RESET_HAND = "reset_hand"
    WARRIOR = "warrior"
    BLOOD_SACRIFICE = "blood_sacrifice"
    CRITICAL = "critical"
    TRUE_DAMAGE = "true_damage"
    NEXT_MULTI = "next_multi"
    KAMIKAZE = "kamikaze"
    SPAWN = "spawn"
    HEAL = "heal"
    COPY = "copy"

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

class BuffType(Enum):
    DICE_ROLL = "DiceRoll"
    BUFF = "Buff"
    DEBUFF = "Debuff"
    PERM_BUFF = "PermBuff"
    EMPOWER = "Empower"
    BLOOD = "Blood"
    CRIT_RATE = "CritRate"
    CRIT_DMG = "CritDmg"
    EVADE = "Evade"
    STOP_MOVEMENT = "Stop Movement"

class BackgroundState(Enum):
    DECK_BUILDING = "deckbuilding"
    BATTLE = "battle"