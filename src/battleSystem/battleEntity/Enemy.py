from src.battleSystem.battleEntity.Entity import Entity
from src.dependency import *

class Enemy(Entity):
    def __init__(self, name, animationlist):
        super().__init__(name, animationlist, 1200, ENTITY_Y)
        self.health = 6  # Example additional attribute for Enemy

    def update(self, dt):
        super().update(dt)
        # Implement enemy-specific update logic here
        pass

    def render(self, screen, x, y):
        # Call the parent render method
        super().render(screen, x, y)
        # Add enemy-specific rendering logic here if needed
        pass