from src.battleSystem.battleEntity.Enemy import Enemy


class Boss(Enemy):
    def __init__(self, name):
        super().__init__(name)
        # Example additional attribute for Boss
    
    # def moveDecision(self, availableMoveTile, field, player):
    #     selectMoveTile = 0
    #     randomLeft = []
    #     randomRight = []
    #     for index in range(len(availableMoveTile)):
    #         if (not field[availableMoveTile[index]].is_occupied()) or (availableMoveTile[index] == self.fieldTile_index):
    #             if availableMoveTile[index] <= self.fieldTile_index:
    #                 randomLeft.append(index)
    #             if availableMoveTile[index] >= self.fieldTile_index:
    #                 randomRight.append(index)
    #     if self.fieldTile_index > player.fieldTile_index:
    #         selectMoveTile = random.choice(randomLeft)
    #     else:
    #         selectMoveTile = random.choice(randomRight)
    #     if len(availableMoveTile) == 9:
    #         if player.fieldTile_index <= 4:
    #             selectMoveTile = 8
    #         else:
    #             selectMoveTile = 0
    #     return selectMoveTile
    
    def pullDecision(self, availablePullTile, field, player):
        selectPullTile = 0
        # randomPull = []
        # for index in range(len(availablePullTile)):
        #     if (not field[availablePullTile[index]].is_occupied()) or (availablePullTile[index] == player.fieldTile_index):
        #         randomPull.append(index)
        # selectPullTile = random.choice(randomPull)
        return selectPullTile
    
    def pushDecision(self, availablePushTile, field, player):
        selectPushTile = 0
        # randomPush = []
        # for index in range(len(availablePushTile)):
        #     if (not field[availablePushTile[index]].is_occupied()) or (availablePushTile[index] == player.fieldTile_index):
        #         randomPush.append(index)
        # selectPushTile = random.choice(randomPush)
        return selectPushTile

    def update(self, dt, events):
        # Implement boss-specific update logic here
        pass

    def render(self, screen, x, y):
        # Call the parent render method
        super().render(screen, x, y)
        # Add boss-specific rendering logic here if needed
        pass
