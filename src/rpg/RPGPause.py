import sys
import pygame
from src.constants import *
from src.resources import *
from src.EnumResources import *
from src.components.Selector import Selector

class RPGPauseHandler:
    def __init__(self, from_state):
        self.pause_selectors = [
            Selector("edit_deck", y=290, scale=1.0, center=True),
            Selector("inventory", y=350, scale=1.0, center=True),
            Selector("return_to_title", y=410, scale=1.0, center=True)
        ]
        self.pause = False
        self.selected_pause_index = 0
        self.from_state = from_state

    def pause_game(self):
        self.pause = True

    def is_paused(self):
        return self.pause
    
    def update(self, dt, events, params, player):
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
                    if self.pause_selectors[self.selected_pause_index].name == "edit_deck":
                        self.pause = False
                        self.selected_pause_index = 0
                        params['battleSystem'] = {
                            'player': player.battlePlayer,
                            'enemy': None,
                            'edit_player_deck': True,
                            'from_state': self.from_state
                        }
                        g_state_manager.Change(BattleState.DECK_BUILDING, params)
                    elif self.pause_selectors[self.selected_pause_index].name == "inventory":
                        self.pause = False
                        self.selected_pause_index = 0
                        # TODO: wait for inventory
                        return 'inventory'
                        # self.reset_battle(params)
                        # g_state_manager.Change(BattleState.PREPARATION_PHASE, params)
                    elif self.pause_selectors[self.selected_pause_index].name == "return_to_title":
                        self.pause = False
                        self.selected_pause_index = 0
                        g_state_manager.Change(GameState.TITLE, {})
                    
        for idx, selector in enumerate(self.pause_selectors):
            selector.set_active(idx == self.selected_pause_index)

    def render(self, screen):
        if not self.pause:
            return
        # Create a semi-transparent overlay
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)  
        overlay.fill((0, 0, 0, 200))  
        screen.blit(overlay, (0, 0))
    
        if self.pause:
            for selector in self.pause_selectors:
                selector.draw(screen)