import pygame

pygame.mixer.pre_init(44100, -16, 2, 4096)
pygame.init()
music_channel = pygame.mixer.Channel(0)
music_channel.set_volume(0.2)

from src.dependency import *

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
                RPGState.TAVERN: TavernMapState()
        }

        # Set initial states for battle mode
        g_state_manager.SetStates(self.states)

    def StartScreen(self):
        self.screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 74)
        text_rpg = font.render("Press R for RPG Mode", True, (255, 255, 255))
        text_battle = font.render("Press B for Battle Mode", True, (255, 255, 255))
        self.screen.blit(text_rpg, (100, 200))
        self.screen.blit(text_battle, (100, 300))
        pygame.display.flip()

    def PlayGame(self):
        clock = pygame.time.Clock()

        while True:
            dt = clock.tick(self.max_frame_rate) / 1000.0
            events = pygame.event.get()

            # Start screen state
            if self.state == "start":
                self.StartScreen()
                for event in events:
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            # Change to RPG state and set RPG start state in state manager
                            self.state = "rpg"
                            g_state_manager.Change(RPGState.START,{})  # Initialize TownState
                        elif event.key == pygame.K_b:
                            # Change to Battle state and set initial battle phase in state manager
                            self.state = "battle"
                            params = {
                                'battleSystem': {
                                    'player': None,
                                    'enemy': None
                                }
                            }
                            g_state_manager.Change(BattleState.PREPARATION_PHASE, params)

            else:
                g_state_manager.update(dt, events)
                g_state_manager.render()
                pygame.display.update()

if __name__ == '__main__':
    main = GameMain()
    main.PlayGame()
