import pygame
from src.constants import *

pygame.init()

from src.dependency import *

class GameMain:
    def __init__(self):
        self.max_frame_rate = 60
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        g_state_manager.SetScreen(self.screen)

        states = {
            "select": SelectState(),
            # "action": ActionState(),
            # "end": EndState()
        }
        g_state_manager.SetStates(states)

    def PlayGame(self):
        clock = pygame.time.Clock()
        g_state_manager.Change('select', {
        })

        while True:
            dt = clock.tick(self.max_frame_rate) / 1000.0

            #input
            events = pygame.event.get()

            #update
            g_state_manager.update(dt, events)

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