import pygame
pygame.mixer.pre_init(44100, -16, 2, 4096)
pygame.init()
music_channel = pygame.mixer.Channel(0)
music_channel.set_volume(0.2)

from src.dependency import *
from src.Render import *

class GameMain:
    def __init__(self):
        self.max_frame_rate = 60
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        g_state_manager.SetScreen(self.screen)

        # Define battle, RPG, and title states
        self.states = {
            BattleState.DECK_BUILDING: DeckBuildingState(),
            BattleState.PREPARATION_PHASE: BattlePreparationState(),
            BattleState.INITIAL_PHASE: BattleInitialState(),
            BattleState.SELECTION_PHASE: BattleSelectState(),
            BattleState.ACTION_PHASE: BattleActionState(),
            BattleState.RESOLVE_PHASE: BattleResolveState(),
            SelectionState.ATTACK: SelectAttackState(),
            SelectionState.BUFF: SelectBuffState(),
            SelectionState.MOVE: SelectMoveState(),
            SelectionState.PUSH: SelectPushState(),
            SelectionState.PULL: SelectPullState(),
            SelectionState.SPAWN: SelectSpawnState(),
            BattleState.END_PHASE: BattleEndState(),
            BattleState.FINISH_PHASE: BattleFinishState(),
            RPGState.START: TutorialState(),
            RPGState.INTRO: IntroState(),
            RPGState.TOWN: TownState(),
            RPGState.TAVERN: TavernMapState(),
            RPGState.GOBLIN: GoblinMapState(),
            GameState.TITLE: TitleState()
        }

        # Set initial states for battle mode
        g_state_manager.SetStates(self.states)
        g_state_manager.Change(GameState.TITLE, {})

    def play_game(self):
        clock = pygame.time.Clock()

        while True:
            dt = clock.tick(self.max_frame_rate) / 1000.0

            # Update and render the current game state
            events = pygame.event.get()
            g_state_manager.update(dt, events)
            g_state_manager.render()
            pygame.display.update()

if __name__ == '__main__':
    main = GameMain()
    main.play_game()
