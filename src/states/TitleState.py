import pygame
from src.Render import RenderBackground
from src.components.Selector import Selector
from src.dependency import *
from src.states.BaseState import BaseState
import sys

class TitleState(BaseState):
    def __init__(self):
        super(TitleState, self).__init__()
        self.selectors = [
            Selector("start", y=400, scale=1.2, center=True),
            Selector("quickplay", y=475, scale=1.2, center=True),
            Selector("exit", y=550, scale=1.2, center=True)
        ]
        self.selected_index = 0

    def Enter(self, params=None):
        print("\n>>>>>> Enter TitleState <<<<<<")
        play_music("title_bgm")

    def Exit(self):
        pass

    def update(self, dt, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Navigate using arrow keys
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.selected_index = (self.selected_index + 1) % len(self.selectors)
                elif event.key == pygame.K_UP:
                    self.selected_index = (self.selected_index - 1) % len(self.selectors)
                elif event.key == pygame.K_RETURN:
                    selected_selector = self.selectors[self.selected_index]
                    if selected_selector.name == "start":
                        g_state_manager.Change(RPGState.START, {})
                    elif selected_selector.name == "quickplay":
                        params = {
                            'battleSystem': {
                                'player': None,
                                'enemy': None
                            }
                        }
                        g_state_manager.Change(BattleState.PREPARATION_PHASE, params)
                    elif selected_selector.name == "exit":
                        pygame.quit()
                        sys.exit()

    def render(self, screen):
        # Render background for the title screen
        RenderBackground(screen, BackgroundState.TITLE)
        
        # Highlight the selected option using set_active
        for idx, selector in enumerate(self.selectors):
            selector.set_active(idx == self.selected_index)

        # Draw the updated selectors
        for selector in self.selectors:
            selector.draw(screen)
