import sys
import pygame
from src.constants import *
from src.resources import *
from src.EnumResources import *
from src.components.Selector import Selector

class PauseHandler:
    def __init__(self):
        self.pause_selectors = [
            Selector("resume", y=290, scale=1.0, center=True),
            Selector("restart", y=350, scale=1.0, center=True),
            Selector("return_to_title", y=410, scale=1.0, center=True)
        ]
        self.pause = False
        self.selected_pause_index = 0
    
    def reset(self):
        self.pause = False
        self.selected_pause_index = 0
        for selector in self.pause_selectors:
            selector.set_active(False)

    def pause_game(self):
        self.pause = True

    def is_paused(self):
        return self.pause
        
    def update(self, dt, events, params):
        if not self.pause:
            return
        
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.pause = False
                    return
                elif event.key == pygame.K_DOWN:
                    self.selected_pause_index = (self.selected_pause_index + 1) % len(self.pause_selectors)
                elif event.key == pygame.K_UP:
                    self.selected_pause_index = (self.selected_pause_index - 1) % len(self.pause_selectors)
                elif event.key == pygame.K_RETURN:
                    if self.pause_selectors[self.selected_pause_index].name == "resume":
                        self.pause = False
                        return
                    elif self.pause_selectors[self.selected_pause_index].name == "restart":
                        self.pause = False
                        self.selected_pause_index = 0
                        # TODO: reset game details
                        g_state_manager.Change(BattleState.PREPARATION_PHASE, params)
                    elif self.pause_selectors[self.selected_pause_index].name == "return_to_title":
                        self.pause = False
                        self.selected_pause_index = 0
                        g_state_manager.Change(GameState.TITLE, params)
                    
        for idx, selector in enumerate(self.pause_selectors):
            selector.set_active(idx == self.selected_pause_index)

    def draw(self, screen):
        if not self.pause:
            return
        # Create a semi-transparent overlay
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)  
        overlay.fill((0, 0, 0, 150))  
        screen.blit(overlay, (0, 0))
    
        if self.pause:
            for selector in self.pause_selectors:
                selector.draw(screen)