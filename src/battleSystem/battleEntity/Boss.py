import random
from src.EnumResources import PlayerType
from src.battleSystem.battleEntity.Enemy import Enemy


class Boss(Enemy):
    def __init__(self, name, animationlist):
        super().__init__(name, animationlist)
        # Example additional attribute for Boss
    
    def moveDecision(self, availableMoveTile, field, player, currentTurnOwner):
        selectMoveTile = 0
        #start with the random select in case not have the logical index to select
        randomMove = []
        for index in range(len(availableMoveTile)):
            if (not field[availableMoveTile[index]].is_occupied()) or (availableMoveTile[index] == self.fieldTile_index):
                randomMove.append(index)
        selectMoveTile = random.choice(randomMove)
        # then the logical select
        # select the place that can attack player
        for index in range(len(availableMoveTile)):
                if (not field[availableMoveTile[index]].is_occupied()) or (availableMoveTile[index] == self.fieldTile_index):
                    if (player.fieldTile_index <= availableMoveTile[index] + self.selectedCard.range_end and player.fieldTile_index >= availableMoveTile[index] + self.selectedCard.range_start) or (player.fieldTile_index >= availableMoveTile[index] - self.selectedCard.range_end and player.fieldTile_index <= availableMoveTile[index]- self.selectedCard.range_start):
                        selectMoveTile = index
        #better if enemy can avoid player
        for index in range(len(availableMoveTile)):
            if (not field[availableMoveTile[index]].is_occupied()) or (availableMoveTile[index] == self.fieldTile_index):
                # avoid player attack range first
                if not ((availableMoveTile[index]<= player.fieldTile_index + player.selectedCard.range_end and availableMoveTile[index] >= player.fieldTile_index + player.selectedCard.range_start) or (availableMoveTile[index] >= player.fieldTile_index - player.selectedCard.range_end and availableMoveTile[index] <= player.fieldTile_index - player.selectedCard.range_start)):
                    # then also favored if can also attack player
                    if (player.fieldTile_index <= availableMoveTile[index] + self.selectedCard.range_end and player.fieldTile_index >= availableMoveTile[index] + self.selectedCard.range_start) or (player.fieldTile_index >= availableMoveTile[index] - self.selectedCard.range_end and player.fieldTile_index <= availableMoveTile[index]- self.selectedCard.range_start):
                        selectMoveTile = index
                        break

        #effect of backup card i think only this card has range of all the board
        if len(availableMoveTile) == 9:
            if player.fieldTile_index <= 4:
                selectMoveTile = 8
            else:
                selectMoveTile = 0
        return selectMoveTile
    
    def pullDecision(self, availablePullTile, field, player, currentTurnOwner):
        selectPullTile = 0
        #start with the random select in case not have the logical index to select
        randomPull = []
        for index in range(len(availablePullTile)):
            if (not field[availablePullTile[index]].is_occupied()) or (availablePullTile[index] == player.fieldTile_index):
                randomPull.append(index)
        selectPullTile = random.choice(randomPull)
        # then the logical select
        #if start before player
        if self.speed > player.speed or ((self.speed == player.speed) and currentTurnOwner == PlayerType.ENEMY):
            for index in range(len(availablePullTile)):
                if (not field[availablePullTile[index]].is_occupied()) or (availablePullTile[index] == player.fieldTile_index):
                    #pull player into enemy attack range
                    if (availablePullTile[index] <= self.fieldTile_index + self.selectedCard.range_end and availablePullTile[index] >= self.fieldTile_index + self.selectedCard.range_start) or (availablePullTile[index] >= self.fieldTile_index - self.selectedCard.range_end and availablePullTile[index] <= self.fieldTile_index - self.selectedCard.range_start):
                        selectPullTile = index
                        # more favored if the pulled tile not being in the attack range of player
                        if not ((self.fieldTile_index <= availablePullTile[index] + player.selectedCard.range_end and self.fieldTile_index >= availablePullTile[index] + player.selectedCard.range_start) or (self.fieldTile_index >= availablePullTile[index] - player.selectedCard.range_end and self.fieldTile_index <= availablePullTile[index] - player.selectedCard.range_start)):
                            break
        #if start after player              
        else:
            for index in range(len(availablePullTile)):
                if (not field[availablePullTile[index]].is_occupied()) or (availablePullTile[index] == player.fieldTile_index):
                    if (availablePullTile[index] <= self.fieldTile_index + self.selectedCard.range_end and availablePullTile[index] >= self.fieldTile_index + self.selectedCard.range_start) or (availablePullTile[index] >= self.fieldTile_index - self.selectedCard.range_end and availablePullTile[index] <= self.fieldTile_index - self.selectedCard.range_start):
                        selectPullTile = index
       
        return selectPullTile
    
    def pushDecision(self, availablePushTile, field, player, currentTurnOwner):
        selectPushTile = 0
        #start with the random select in case not have the logical index to select
        randomPush = []
        for index in range(len(availablePushTile)):
            if (not field[availablePushTile[index]].is_occupied()) or (availablePushTile[index] == player.fieldTile_index):
                randomPush.append(index)
        selectPushTile = random.choice(randomPush)
        # then the logical select
        #if start before player
        if self.speed > player.speed or ((self.speed == player.speed) and currentTurnOwner == PlayerType.ENEMY):
            for index in range(len(availablePushTile)):
                if (not field[availablePushTile[index]].is_occupied()) or (availablePushTile[index] == player.fieldTile_index):
                    #push player into enemy attack range
                    if (availablePushTile[index] <= self.fieldTile_index + self.selectedCard.range_end and availablePushTile[index] >= self.fieldTile_index + self.selectedCard.range_start) or (availablePushTile[index] >= self.fieldTile_index - self.selectedCard.range_end and availablePushTile[index] <= self.fieldTile_index - self.selectedCard.range_start):
                        selectPushTile = index
                        # more favored if the pulled tile not being in the attack range of player
                        if not ((self.fieldTile_index <= availablePushTile[index] + player.selectedCard.range_end and self.fieldTile_index >= availablePushTile[index] + player.selectedCard.range_start) or (self.fieldTile_index >= availablePushTile[index] - player.selectedCard.range_end and self.fieldTile_index <= availablePushTile[index] - player.selectedCard.range_start)):
                            break
        #if start after player              
        else:
            for index in range(len(availablePushTile)):
                if (not field[availablePushTile[index]].is_occupied()) or (availablePushTile[index] == player.fieldTile_index):
                    if (availablePushTile[index] <= self.fieldTile_index + self.selectedCard.range_end and availablePushTile[index] >= self.fieldTile_index + self.selectedCard.range_start) or (availablePushTile[index] >= self.fieldTile_index - self.selectedCard.range_end and availablePushTile[index] <= self.fieldTile_index - self.selectedCard.range_start):
                        selectPushTile = index
        return selectPushTile

    # def update(self, dt, events):
    #     # Implement boss-specific update logic here
    #     pass

    # def render(self, screen, x, y):
    #     # Call the parent render method
    #     super().render(screen, x, y)
    #     # Add boss-specific rendering logic here if needed
    #     pass
