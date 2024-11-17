import sys
import pygame
from src.constants import *
from src.resources import *
from src.EnumResources import *
from src.components.Selector import Selector

class RPGPauseHandler:
    def __init__(self):
        self.pause_selectors = [
            Selector("edit_deck", y=290, scale=1.0, center=True),
            # TODO: wait for inventory
            Selector("quickplay", y=350, scale=1.0, center=True),
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
        
    def reset_battle(self, params):
        # Safely access the 'battleSystem' dictionary, return if it doesn't exist
        battle_param = params.get('battleSystem')
        if not battle_param:
            print("Battle system parameters missing, skipping reset.")
            return

        # Check for each component and do nothing if they don't exist
        player = battle_param.get('player')
        enemy = battle_param.get('enemy')
        field = battle_param.get('field')

        if not player or not enemy or not field:
            print("Missing player, enemy, or field. Skipping reset.")
            return

        # Reset player and enemy if they exist
        player.reset_everything()
        enemy.reset_everything()

        # Reset each field tile if field is not empty
        for fieldtile in field:
            if fieldtile:  # Check if the field tile is valid
                fieldtile.remove_entity()
                fieldtile.remove_second_entity()

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
                            'from_state': RPGState.TOWN
                        }
                        g_state_manager.Change(BattleState.DECK_BUILDING, params)
                    elif self.pause_selectors[self.selected_pause_index].name == "quickplay":
                        self.pause = False
                        self.selected_pause_index = 0
                        # TODO: wait for inventory
                        return 'inventory'
                        # self.reset_battle(params)
                        # g_state_manager.Change(BattleState.PREPARATION_PHASE, params)
                    elif self.pause_selectors[self.selected_pause_index].name == "return_to_title":
                        self.pause = False
                        self.selected_pause_index = 0
                        self.reset_battle(params) 
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