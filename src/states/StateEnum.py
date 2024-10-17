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

class PlayerType(Enum):
    PLAYER = 1
    ENEMY = 2