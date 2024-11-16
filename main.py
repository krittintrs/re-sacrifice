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
        self.state = GameState.START  # Start with the start screen

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
            RPGState.START: TutorialState(),
            RPGState.INTRO: IntroState(),
            RPGState.TOWN: TownState(),
            RPGState.TAVERN: TavernMapState(),
            RPGState.GOBLIN: GoblinMapState()
        }

        # Set initial states for battle mode
        g_state_manager.SetStates(self.states)

        # Initialize selectors
        self.selectors = [
            Selector("start", y=400, scale=1.2, center=True),
            Selector("quickplay", y=475, scale=1.2, center=True),
            Selector("exit", y=550, scale=1.2, center=True)
        ]
        self.selected_index = 0

    def start_screen(self):
        """Handles rendering and input for the start screen."""
        RenderBackground(self.screen, BackgroundState.TITLE)

        # Highlight the selected option using set_active
        for idx, selector in enumerate(self.selectors):
            selector.set_active(idx == self.selected_index)

        # Draw the updated selectors
        for selector in self.selectors:
            selector.draw(self.screen)

        pygame.display.update()

        # Handle events for start screen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

            # Navigate using arrow keys
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.selected_index = (self.selected_index + 1) % len(self.selectors)
                elif event.key == pygame.K_UP:
                    self.selected_index = (self.selected_index - 1) % len(self.selectors)
                elif event.key == pygame.K_RETURN:
                    selected_selector = self.selectors[self.selected_index]
                    if selected_selector.name == "start":
                        self.state = GameState.RPG
                        g_state_manager.Change(RPGState.START, {})
                    elif selected_selector.name == "quickplay":
                        self.state = GameState.BATTLE
                        params = {
                            'battleSystem': {
                                'player': None, 
                                'enemy': None
                            }
                        }
                        g_state_manager.Change(BattleState.PREPARATION_PHASE, params)
                    elif selected_selector.name == "exit":
                        pygame.quit()
                        return False
        return True

    def play_game(self):
        clock = pygame.time.Clock()

        while True:
            dt = clock.tick(self.max_frame_rate) / 1000.0

            if self.state == GameState.START:
                if not self.start_screen():
                    return
            else:
                # Update and render the current game state
                events = pygame.event.get()
                g_state_manager.update(dt, events)
                g_state_manager.render()
                pygame.display.update()

if __name__ == '__main__':
    main = GameMain()
    main.play_game()
