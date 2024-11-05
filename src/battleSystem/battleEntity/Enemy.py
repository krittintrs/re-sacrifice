from src.battleSystem.battleEntity.Entity import Entity

class Enemy(Entity):
    def __init__(self, name, animationlist):
        super().__init__(name, animationlist)
        self.health = 6  # Example additional attribute for Enemy

    def update(self, dt, events):
        # Implement enemy-specific update logic here
        pass

    def render(self, screen, x, y):
        # Call the parent render method
        super().render(screen, x -185, y - 185)
        # Add enemy-specific rendering logic here if needed
        pass