from src.battleSystem.battleEntity.Entity import Entity
from src.dependency import *
from src.battleSystem.Effect import Effect


class Player(Entity):
    def __init__(self, conf):
        self.job = conf.job
        self.loadClassAnimation()
        super().__init__(conf.name, conf.deckInv, self.animationList, 0, ENTITY_Y, gVfx_animation_list)
        self.health = 30
        self.maxhealth = 30
        self.x, self.y = 0, ENTITY_Y
        self.type = PlayerType.PLAYER

    def loadClassAnimation(self):
        if self.job == PlayerClass.WARRIOR:
            self.animationList = gWarrior_animation_list
        elif self.job == PlayerClass.RANGER:
            self.animationList = gRanger_animation_list
        elif self.job == PlayerClass.MAGE:
            self.animationList = gMage_animation_list

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
