import random
from src.states.BaseState import BaseState
from src.dependency import *
from src.constants import *
from src.Render import *
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

        self.availableMoveTile = []

        if self.effectOwner == PlayerType.PLAYER:
            for buff in self.player.buffs:
                if buff.name == "Stop Movement":
                    print("can not move due to debuff")
                    self.leftSkip = True
                    self.rightSkip = True
                    break
            startIndex = self.player.fieldTile_index
            self.leftMinTileIndex = self.player.fieldTile_index - self.effect.minRange
            self.leftMaxTileIndex = self.player.fieldTile_index - self.effect.maxRange
            self.rightMinTileIndex = self.player.fieldTile_index + self.effect.minRange
            self.rightMaxTileIndex = self.player.fieldTile_index + self.effect.maxRange
            print("should still run this code though")
        elif self.effectOwner == PlayerType.ENEMY:
            for buff in self.enemy.buffs:
                if buff.name == "Stop Movement":
                    print("can not move due to debuff")
                    self.leftSkip = True
                    self.rightSkip = True
                    break
            startIndex = self.enemy.fieldTile_index
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
                self.availableMoveTile.append(i)
        
        for j in range(self.rightMinTileIndex, self.rightMaxTileIndex+1):
            if not self.rightSkip:
                self.availableMoveTile.append(j)

        # restrict available move space due to trap
        for idx,index in enumerate(self.availableMoveTile):
            tile = self.field[index]
            if tile.is_second_entity() and tile.second_entity.side != self.effectOwner:
                if index < startIndex: # trap is on the left of entity
                    self.availableMoveTile = self.availableMoveTile[idx:]
                if index > startIndex:
                    self.availableMoveTile = self.availableMoveTile[:idx]

        
        self.availableMoveTile = list( dict.fromkeys(self.availableMoveTile) )
        
        print('\n!!!! SelectMoveState !!!!')
        print(f'Owner: {self.effectOwner}')
        print(f'Effect: {self.effect.type} ({self.effect.minRange} - {self.effect.maxRange})')
        print(f'SelectMoveTile: {self.selectMoveTile}')

        if self.effectOwner == PlayerType.ENEMY:
            randomLeft = []
            randomRight = []
            for index in range(len(self.availableMoveTile)):
                if not self.field[self.availableMoveTile[index]].is_occupied():
                    if self.availableMoveTile[index] <= self.enemy.fieldTile_index:
                        randomLeft.append(index)
                    if self.availableMoveTile[index] >= self.enemy.fieldTile_index:
                        randomRight.append(index)
            if self.enemy.fieldTile_index > self.player.fieldTile_index:
                self.selectMoveTile = random.choice(randomLeft)
            else:
                self.selectMoveTile = random.choice(randomRight)
        
        # apply buff to all cards on hand
        self.player.apply_buffs_to_cardsOnHand()
        self.enemy.apply_buffs_to_cardsOnHand()

        # display entity stats
        self.player.display_stats()
        self.enemy.display_stats()

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
                    print('key left')
                    if self.effectOwner == PlayerType.PLAYER:
                        print('moving left')
                        self.selectMoveTile = self.selectMoveTile - 1
                        if self.selectMoveTile < 0:
                            self.selectMoveTile = len(self.availableMoveTile) - 1
                if event.key == pygame.K_RIGHT and self.selectMoveTile>=0:
                    print('key right')
                    if self.effectOwner == PlayerType.PLAYER:
                        print('moving right')
                        self.selectMoveTile = self.selectMoveTile + 1
                        if self.selectMoveTile > len(self.availableMoveTile) - 1:
                            self.selectMoveTile = 0
                if event.key == pygame.K_RETURN:
                    print('move state: before check effect owner')
                    selected_field = self.field[self.availableMoveTile[self.selectMoveTile]]
                    if self.effectOwner == PlayerType.PLAYER:
                        print('player movement')
                        if self.selectMoveTile>=0 and self.effect.maxRange>0:
                            if not selected_field.is_occupied():
                                if selected_field.is_second_entity():
                                    selected_field.second_entity.collide(self.player, selected_field) 
                                self.player.move_to(self.field[self.availableMoveTile[self.selectMoveTile]], self.field)
                                print(f"{self.effectOwner} move to {self.availableMoveTile[self.selectMoveTile]}")
                            else:
                                print("can not move, there is an entity of that tile")
                        else:
                            print("there is no movement happen")
                    else:
                        print("enemy movement")
                        if self.selectMoveTile>=0 and self.effect.maxRange>0:
                            if not selected_field.is_occupied():
                                if selected_field.is_second_entity():
                                    selected_field.second_entity.collide(self.enemy, selected_field)
                                self.enemy.move_to(self.field[self.availableMoveTile[self.selectMoveTile]], self.field)
                                print(f"{self.effectOwner} move to {self.availableMoveTile[self.selectMoveTile]}")
                            else:
                                print("can not move, there is an entity of that tile")
                        else:
                            print("there is no movement happen")
                    print('move state: after check effect owner')
                    if self.player.health > 0 and self.enemy.health > 0:
                        g_state_manager.Change(BattleState.RESOLVE_PHASE, {
                            'player': self.player,
                            'enemy': self.enemy,
                            'field': self.field,
                            'turn': self.turn,
                            'currentTurnOwner': self.currentTurnOwner,
                            'effectOrder': self.effectOrder
                        })
                    else:
                        if self.player.health <= 0:
                            self.winner = PlayerType.ENEMY
                        elif self.enemy.health <= 0:
                            self.winner = PlayerType.PLAYER
                        g_state_manager.Change(BattleState.FINISH_PHASE, {
                            'player': self.player,
                            'enemy': self.enemy,
                            'field': self.field,
                            'turn': self.turn,
                            'currentTurnOwner': self.currentTurnOwner,
                            'winner': self.winner
                        })

        for buff in self.player.buffs:
            buff.update(dt, events)
        for buff in self.enemy.buffs:
            buff.update(dt, events)

        self.player.update(dt)
        self.enemy.update(dt)
        
    def render(self, screen):
        RenderTurn(screen, 'SelectMoveState', self.turn, self.currentTurnOwner)
        RenderEntityStats(screen, self.player, self.enemy)
        RenderSelectedCard(screen, self.player.selectedCard, self.enemy.selectedCard)
        RenderCurrentAction(screen, self.effect, self.effectOwner)

        # Render field
        for fieldTile in self.field:               
            # Render the range of the attack

            if fieldTile.index in set(self.availableMoveTile):
                fieldTile.color = (255,0,0)
            else:
                fieldTile.color = (0,0,0)
            if self.selectMoveTile>=0:
                if fieldTile.index == self.availableMoveTile[self.selectMoveTile]:
                    fieldTile.color = (255,0,255)
                    fieldTile.solid = 0
                
            fieldTile.render(screen)
            fieldTile.color = (0,0,0)
            fieldTile.solid = 1

        