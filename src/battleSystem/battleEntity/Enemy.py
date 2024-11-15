import random
from src.battleSystem.battleEntity.Entity import Entity
from src.dependency import *

class Enemy(Entity):
    def __init__(self, name, animationlist):
        super().__init__(name, animationlist)
        self.health = 10  # Example additional attribute for Enemy
        self.maxhealth = 10
        self.type = PlayerType.ENEMY
        self.x, self.y = 1200, ENTITY_Y  # Initial position for rendering
    
    #after this part is ai
    def moveDecision(self, availableMoveTile, field, player, currentTurnOwner):
        selectMoveTile = 0
        randomLeft = []
        randomRight = []
        for index in range(len(availableMoveTile)):
            if (not field[availableMoveTile[index]].is_occupied()) or (availableMoveTile[index] == self.fieldTile_index):
                if availableMoveTile[index] <= self.fieldTile_index:
                    randomLeft.append(index)
                if availableMoveTile[index] >= self.fieldTile_index:
                    randomRight.append(index)
        if self.fieldTile_index > player.fieldTile_index:
            selectMoveTile = random.choice(randomLeft)
        else:
            selectMoveTile = random.choice(randomRight)
        if len(availableMoveTile) == 9:
            if player.fieldTile_index <= 4:
                selectMoveTile = 8
            else:
                selectMoveTile = 0
        return selectMoveTile
    
    def attackDecision(self, availableAttackTile, field, player):
        selectAttackTile = 0
        for index in range(len(availableAttackTile)):
                if field[availableAttackTile[index]].is_occupied():
                    if field[availableAttackTile[index]].entity == player:
                        selectAttackTile = index
        return selectAttackTile
    
    def oppoBuffDecision(self, availableBuffTile, field, player):
        selectBuffTile = 0
        for index in range(len(availableBuffTile)):
                if field[availableBuffTile[index]].is_occupied():
                    if field[availableBuffTile[index]].entity == player:
                        selectBuffTile = index
        return selectBuffTile
    
    def pullDecision(self, availablePullTile, field, player, currentTurnOwner):
        selectPullTile = 0
        randomPull = []
        for index in range(len(availablePullTile)):
            if (not field[availablePullTile[index]].is_occupied()) or (availablePullTile[index] == player.fieldTile_index):
                randomPull.append(index)
        selectPullTile = random.choice(randomPull)
        return selectPullTile
    
    def pushDecision(self, availablePushTile, field, player, currentTurnOwner):
        selectPushTile = 0
        randomPush = []
        for index in range(len(availablePushTile)):
            if (not field[availablePushTile[index]].is_occupied()) or (availablePushTile[index] == player.fieldTile_index):
                randomPush.append(index)
        selectPushTile = random.choice(randomPush)
        return selectPushTile

    def update(self, dt):
        super().update(dt)
        # Implement enemy-specific update logic here
        pass

    def render(self, screen, x, y):
        # Call the parent render method
        super().render(screen, x, y)
        # Add enemy-specific rendering logic here if needed
        pass