from src.battleSystem.battleEntity.Entity import Entity
from src.dependency import *

class Enemy(Entity):
    def __init__(self, conf):
        super().__init__(conf.name, conf.deckInv, conf.animationList, 1200, ENTITY_Y, gVfx_animation_list)
        self.health = 30  # Example additional attribute for Enemy
        self.maxhealth = 30
        self.type = PlayerType.ENEMY
        self.x, self.y = 1200, ENTITY_Y  # Initial position for rendering

    def update(self, dt):
        super().update(dt)
        # Implement enemy-specific update logic here
        pass

    def render(self, screen, x, y):
        # Call the parent render method
        super().render(screen, x, y)
        # Add enemy-specific rendering logic here if needed
        pass