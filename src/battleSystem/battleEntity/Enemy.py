from src.battleSystem.battleEntity.Entity import Entity

class Enemy(Entity):
    def __init__(self, name, image=None):
        super().__init__(name, image)
        self.health = 100  # Example additional attribute for Enemy

    def update(self, dt, events):
        # Implement enemy-specific update logic here
        pass

    def render(self, screen, x, y):
        # Call the parent render method
        super().render(screen, x, y)
        # Add enemy-specific rendering logic here if needed
        pass