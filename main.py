import pygame
from src.dependency import *

pygame.init()

from src.dependency import *

class GameMain:
    def __init__(self):
        self.max_frame_rate = 60
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        g_state_manager.SetScreen(self.screen)

        states = {
            "prepare": BattlePreparationState(),
            "deck":DeckBuildingState(),
            "initial": BattleInitialState(),
            "select": BattleSelectState(),
            "action": BattleActionState(),
            "end": BattleEndState(),
            "finish": BattleFinishState()
        }
        g_state_manager.SetStates(states)

    def RenderBackground(self):
        self.screen.fill((255, 255, 255))
        self.CreateBattleField(self.screen)

    def CreateBattleField(self, screen):
        # Draw the HUD background (full width, height 200 at the bottom)
        
        # Dark grey background for HUD
        pygame.draw.rect(screen, (50, 50, 50), (0, SCREEN_HEIGHT  - HUD_HEIGHT, SCREEN_WIDTH, HUD_HEIGHT))                     

    def PlayGame(self):
        clock = pygame.time.Clock()
        g_state_manager.Change('prepare', {
        })

        while True:
            dt = clock.tick(self.max_frame_rate) / 1000.0

            #input
            events = pygame.event.get()

            #update
            g_state_manager.update(dt, events)

            #bg render
            self.RenderBackground()
            #render
            g_state_manager.render()
            
            #screen update
            pygame.display.update()

            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

if __name__ == '__main__':
    main = GameMain()

    main.PlayGame()