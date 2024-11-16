import pygame

pygame.mixer.pre_init(44100, -16, 2, 4096)
pygame.init()
music_channel = pygame.mixer.Channel(0)
music_channel.set_volume(0.2)

from src.dependency import *
from src.Render import *
from src.components.Selector import Selector

class GameMain:
    def __init__(self):
        self.max_frame_rate = 60
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        g_state_manager.SetScreen(self.screen)
        self.state = "start"  # Start with the start screen

        # Define battle and RPG states
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
                RPGState.START: TutorialState(),# Add RPG start state here
                RPGState.INTRO: IntroState(),
                RPGState.TOWN: TownState(),
                RPGState.TAVERN: TavernMapState(),
                RPGState.GOBLIN: GoblinMapState()
        }

        # Set initial states for battle mode
        g_state_manager.SetStates(self.states)

    def StartScreen(self):
        RenderBackground(self.screen, BackgroundState.TITLE)

        # Initialize selectors with positions
        start_selector = Selector("start", y=400, scale=1.2, center=True)
        quickplay_selector = Selector("quickplay", y=475, scale=1.2, center=True)
        exit_selector = Selector("exit", y=550, scale=1.2, center=True)
        
        # Draw selectors
        start_selector.draw(self.screen)
        quickplay_selector.draw(self.screen)
        exit_selector.draw(self.screen)

        pygame.display.flip()

        return start_selector, quickplay_selector, exit_selector

    def PlayGame(self):
        clock = pygame.time.Clock()

        while True:
            dt = clock.tick(self.max_frame_rate) / 1000.0
            events = pygame.event.get()

            # Start screen state
            if self.state == "start":
                start_selector, quickplay_selector, exit_selector = self.StartScreen()
                for event in events:
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return

                if start_selector.is_clicked():
                    self.state = "rpg"
                    g_state_manager.Change(RPGState.START, {})  # Initialize TownState

                if quickplay_selector.is_clicked():
                    self.state = "battle"
                    params = {
                        'battleSystem': {
                            'player': None,
                            'enemy': None
                        }
                    }
                    g_state_manager.Change(BattleState.PREPARATION_PHASE, params)

                if exit_selector.is_clicked():
                    pygame.quit()
                    return

            else:
                g_state_manager.update(dt, events)
                g_state_manager.render()
                pygame.display.update()

if __name__ == '__main__':
    main = GameMain()
    main.PlayGame()
