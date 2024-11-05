from src.states.BaseState import BaseState
from src.dependency import *
from src.constants import *
import pygame
import sys

class SelectMoveState(BaseState):
    def __init__(self):
        super(SelectMoveState, self).__init__()

    def Enter(self, params):
        self.player = params['player']
        self.enemy = params['enemy']
        self.field = params['field']
        self.turn = params['turn']
        self.currentTurnOwner = params['currentTurnOwner']  
        self.effectOrder = params['effectOrder']
        self.effect = params['effect']
        self.effectOwner = params['effectOwner']
        
        self.leftSkip = False
        self.rightSkip = False

        self.avilableMoveTile = []

        if self.effectOwner == PlayerType.PLAYER:
            self.leftMinTileIndex = self.player.fieldTile_index - self.effect.minRange
            self.leftMaxTileIndex = self.player.fieldTile_index - self.effect.maxRange
            self.rightMinTileIndex = self.player.fieldTile_index + self.effect.minRange
            self.rightMaxTileIndex = self.player.fieldTile_index + self.effect.maxRange 
        elif self.effectOwner == PlayerType.ENEMY: 
            self.leftMinTileIndex = self.enemy.fieldTile_index - self.effect.minRange
            self.leftMaxTileIndex = self.enemy.fieldTile_index - self.effect.maxRange
            self.rightMinTileIndex = self.enemy.fieldTile_index + self.effect.minRange
            self.rightMaxTileIndex = self.enemy.fieldTile_index + self.effect.maxRange        

        if self.leftMinTileIndex < 0:
            self.leftMinTileIndex = 0
            self.leftMaxTileIndex = 0
            self.leftSkip = True
        elif self.leftMaxTileIndex < 0:
            self.leftMaxTileIndex = 0

        if self.rightMinTileIndex > 8:
            self.rightMinTileIndex = 8
            self.rightMaxTileIndex = 8
            self.rightSkip = True
        elif self.rightMaxTileIndex > 8:
            self.rightMaxTileIndex = 8
        
        self.selectMoveTile = 0
        if self.rightSkip and self.leftSkip:
                self.selectMoveTile = -1

        for i in range(self.leftMaxTileIndex, self.leftMinTileIndex+1):
            if not self.leftSkip:
                self.avilableMoveTile.append(i)
        
        for j in range(self.rightMinTileIndex, self.rightMaxTileIndex+1):
            if not self.rightSkip:
                self.avilableMoveTile.append(j)
        
        self.avilableMoveTile = list( dict.fromkeys(self.avilableMoveTile) )
        

    def Exit(self):
        pass

    def update(self, dt, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_SPACE:
                    pass
                if event.key == pygame.K_LEFT and self.selectMoveTile>=0:
                    if self.effectOwner == PlayerType.PLAYER:
                        self.selectMoveTile = self.selectMoveTile - 1
                        if self.selectMoveTile < 0:
                            self.selectMoveTile = len(self.avilableMoveTile) - 1
                if event.key == pygame.K_RIGHT and self.selectMoveTile>=0:
                    if self.effectOwner == PlayerType.PLAYER:
                        self.selectMoveTile = self.selectMoveTile + 1
                        if self.selectMoveTile > len(self.avilableMoveTile) - 1:
                            self.selectMoveTile = 0
                if event.key == pygame.K_RETURN:
                    print('!!!! SelectMoveState !!!!')
                    print(f'Owner: {self.effectOwner}')
                    print(f'Effect: {self.effect.type} ({self.effect.minRange} - {self.effect.maxRange})')

                    if self.effectOwner == PlayerType.PLAYER:
                        if self.selectMoveTile>=0 and self.effect.maxRange>0:
                            if not self.field[self.avilableMoveTile[self.selectMoveTile]].is_occupied():
                                self.player.move_to(self.field[self.avilableMoveTile[self.selectMoveTile]], self.field)
                                print(f"{self.effectOwner} move to {self.avilableMoveTile[self.selectMoveTile]}")
                            else:
                                print("can not move, there is an entity of that tile")
                        else:
                            print("there is no movement happen")

                    g_state_manager.Change(BattleState.RESOLVE_PHASE, {
                        'player': self.player,
                        'enemy': self.enemy,
                        'field': self.field,
                        'turn': self.turn,
                        'currentTurnOwner': self.currentTurnOwner,
                        'effectOrder': self.effectOrder
                    })

        for buff in self.player.buffs:
            buff.update(dt, events)
        for buff in self.enemy.buffs:
            buff.update(dt, events)

        self.player.update(dt)

    def render(self, screen):
        # Turn
        screen.blit(pygame.font.Font(None, 36).render(f"SelectMoveState - Turn {self.turn} - {self.effectOwner}", True, (0, 0, 0)), (10, 10))   

        # Render cards on player's hand
        for order, card in enumerate(self.player.cardsOnHand):
            card.render(screen, order)

        # Render field
        for fieldTile in self.field:               
            # Render the range of the attack

            if fieldTile.index in set(self.avilableMoveTile):
                fieldTile.color = (255,0,0)
            else:
                fieldTile.color = (0,0,0)
            if self.selectMoveTile>=0:
                if fieldTile.index == self.avilableMoveTile[self.selectMoveTile]:
                    fieldTile.color = (255,0,255)
                    fieldTile.solid = 0
                
            fieldTile.render(screen, len(self.field))
            fieldTile.color = (0,0,0)
            fieldTile.solid = 1

        