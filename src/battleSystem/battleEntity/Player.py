from src.battleSystem.battleEntity.Entity import Entity


class Player(Entity):
    def __init__(self, name, image=None):
        super().__init__(name, image)
        self.health = 30

    def update(self, dt, events):
        # Implement player-specific update logic here
        pass

    def render(self, screen, x, y):
        # Call the parent render method
        super().render(screen, x, y, (0, 255, 0))
        # Add player-specific rendering logic here if needed
        pass
