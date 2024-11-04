from src.rpg.entity.EntityIdleState import EntityIdleState
import pygame

class PlayerIdleState(EntityIdleState):
    def __init__(self, player):
        super(PlayerIdleState, self).__init__(player)
    def Enter(self, params):
        self.entity.offset_y = 15
        self.entity.offset_x = 0
        super().Enter(params)

    def Exit(self):
        pass

    def update(self, dt, events):
        pressedKeys = pygame.key.get_pressed()
        if pressedKeys[pygame.K_LEFT] or pressedKeys [pygame.K_RIGHT] or pressedKeys [pygame.K_UP] or pressedKeys [pygame.K_DOWN]:
            print("Transitioning to walk state from idle")
            self.entity.ChangeState('walk')

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    print("Space pressed")