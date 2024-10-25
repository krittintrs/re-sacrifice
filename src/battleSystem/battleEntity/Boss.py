from src.battleSystem.battleEntity.Enemy import Enemy


class Boss(Enemy):
    def __init__(self, name, image=None):
        super().__init__(name, image)
        self.attack = 20  # Example additional attribute for Boss

    def update(self, dt, events):
        # Implement boss-specific update logic here
        pass

    def render(self, screen, x, y):
        # Call the parent render method
        super().render(screen, x, y)
        # Add boss-specific rendering logic here if needed
        pass
