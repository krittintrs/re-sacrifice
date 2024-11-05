from src.states.BaseState import BaseState
from src.dependency import *
from src.constants import *
import pygame
import sys

class SelectBuffState(BaseState):
    def __init__(self):
        super(SelectBuffState, self).__init__()

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

        self.avilableBuffTile = []

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
        
        self.selectBuffTile = 0

        if self.rightSkip and self.leftSkip:
                self.selectBuffTile = -1

        for i in range(self.leftMaxTileIndex, self.leftMinTileIndex+1):
            if not self.leftSkip:
                self.avilableBuffTile.append(i)
        
        for j in range(self.rightMinTileIndex, self.rightMaxTileIndex+1):
            if not self.rightSkip:
                self.avilableBuffTile.append(j)
        
        self.avilableBuffTile = list( dict.fromkeys(self.avilableBuffTile) )

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
                    if event.key == pygame.K_LEFT and self.selectBuffTile>=0:
                        if self.effectOwner == PlayerType.PLAYER:
                            self.selectBuffTile = self.selectBuffTile - 1
                            if self.selectBuffTile < 0:
                                self.selectBuffTile = len(self.avilableBuffTile) - 1
                    if event.key == pygame.K_RIGHT and self.selectBuffTile>=0:
                        if self.effectOwner == PlayerType.PLAYER:
                            self.selectBuffTile = self.selectBuffTile + 1
                            if self.selectBuffTile > len(self.avilableBuffTile) - 1:
                                self.selectBuffTile = 0
                if event.key == pygame.K_RETURN:
                    print('!!!! SelectBuffState !!!!')
                    print(f'Owner: {self.effectOwner}')
                    print(f'Effect: {self.effect.type} ({self.effect.minRange} - {self.effect.maxRange})')

                    if self.effectOwner == PlayerType.PLAYER:
                        if self.selectffTile>=0 and self.effect.maxRange>0:
                            if self.field[self.avilableAttackTile[self.selectAttackTile]].is_occupied():
                                print("apply buff")
                            else:
                                print("no entity on the targeted tile")
                        else:
                            print("there is no buff happen")

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
        screen.blit(pygame.font.Font(None, 36).render(f"SelectBuffState - Turn {self.turn}", True, (0, 0, 0)), (10, 10))   
        
        # Render cards on player's hand
        for order, card in enumerate(self.player.cardsOnHand):
            card.render(screen, order)

        # Render field
        for fieldTile in self.field:               
            # Render the range of the buff

            if fieldTile.index in set(self.avilableBuffTile):
                fieldTile.color = (255,0,0)
            else:
                fieldTile.color = (0,0,0)
            if self.selectBuffTile>=0:
                if fieldTile.index == self.avilableBuffTile[self.selectBuffTile]:
                    fieldTile.color = (255,0,255)
                    fieldTile.solid = 0
                
            fieldTile.render(screen, len(self.field))
            fieldTile.color = (0,0,0)
            fieldTile.solid = 1

        