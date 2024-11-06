from src.battleSystem.battleEntity.Entity import Entity
from src.dependency import *


class Player(Entity):
    def __init__(self, name, job, animationList):
        super().__init__(name, animationList)
        self.health = 30
        self.job = job

        self.x, self.y = 0, SCREEN_HEIGHT // 3 - FIELD_HEIGHT // 2  # Initial position for rendering

    def update(self, dt):
        # Implement player-specific update logic here
        super().update(dt)
        pass

    def render(self, screen, x, y):
        # Call the parent render method
        super().render(screen, x, y, (0, 255, 0))

        # Add player-specific rendering logic here if needed
        # screen.blit(self.image, (x, y))
        pass
