import random
from src.states.BaseState import BaseState
from src.dependency import *
from src.constants import *
from src.Render import *
import pygame
import sys

class SelectPushState(BaseState):
    def __init__(self):
        super(SelectPushState, self).__init__()

    def Enter(self, params):
        self.player = params['player']
        self.enemy = params['enemy']
        self.field = params['field']
        self.turn = params['turn']
        self.currentTurnOwner = params['currentTurnOwner']  
        self.effectOrder = params['effectOrder']
        self.effect = params['effect']
        self.effectOwner = params['effectOwner']

        self.availablePushTile = []

        if self.effectOwner == PlayerType.PLAYER:
            if self.player.fieldTile_index > self.enemy.fieldTile_index:
                self.MinTileIndex = self.enemy.fieldTile_index - self.effect.minRange
                self.MaxTileIndex = self.enemy.fieldTile_index - self.effect.maxRange
            else:
                self.MinTileIndex = self.enemy.fieldTile_index + self.effect.minRange
                self.MaxTileIndex = self.enemy.fieldTile_index + self.effect.maxRange 
        elif self.effectOwner == PlayerType.ENEMY: 
            if self.enemy.fieldTile_index > self.player.fieldTile_index:
                self.MinTileIndex = self.player.fieldTile_index - self.effect.minRange
                self.MaxTileIndex = self.player.fieldTile_index - self.effect.maxRange
            else:
                self.MinTileIndex = self.player.fieldTile_index + self.effect.minRange
                self.MaxTileIndex = self.player.fieldTile_index + self.effect.maxRange       


        if self.MaxTileIndex < 0:
            self.MaxTileIndex = 0
        elif self.MaxTileIndex > 8:
            self.MaxTileIndex = 8
        
        self.selectPushTile = 0
        if self.MaxTileIndex <= self.MinTileIndex:
            for i in range(self.MaxTileIndex, self.MinTileIndex+1):
                self.availablePushTile.append(i)
        else:       
            for j in range(self.MinTileIndex, self.MaxTileIndex+1):
                self.availablePushTile.append(j)
        
        self.availablePushTile = list( dict.fromkeys(self.availablePushTile) )
        
        print('\n!!!! SelectPushState !!!!')
        print(f'Owner: {self.effectOwner}')
        print(f'Effect: {self.effect.type} ({self.effect.minRange} - {self.effect.maxRange})')
        print(f'SelectPushTile: {self.selectPushTile}')

        if self.effectOwner == PlayerType.ENEMY:
            randomPush = []
            for index in range(len(self.availablePushTile)):
                if (not self.field[self.availablePushTile[index]].is_occupied()) or (self.availablePushTile[index] == self.player.fieldTile_index):
                    randomPush.append(index)
            self.selectPushTile = random.choice(randomPush)
        
        # apply buff to all cards on hand
        self.player.apply_buffs_to_cardsOnHand()
        self.enemy.apply_buffs_to_cardsOnHand()

        # display entity stats
        self.player.display_stats()
        self.enemy.display_stats()

    def Exit(self):
        pass

    def remove_timeout_entity(self):
        for tile in self.field:
            if tile.is_second_entity():
                if tile.second_entity.duration == 0:
                    print("remove second entity for timeout ", tile.index)
                    tile.remove_second_entity()

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
                if event.key == pygame.K_LEFT:
                    print('key left')
                    if self.effectOwner == PlayerType.PLAYER:
                        print('moving left')
                        self.selectPushTile = self.selectPushTile - 1
                        if self.selectPushTile < 0:
                            self.selectPushTile = len(self.availablePushTile) - 1
                if event.key == pygame.K_RIGHT:
                    print('key right')
                    if self.effectOwner == PlayerType.PLAYER:
                        print('moving right')
                        self.selectPushTile = self.selectPushTile + 1
                        if self.selectPushTile > len(self.availablePushTile) - 1:
                            self.selectPushTile = 0
                if event.key == pygame.K_RETURN:
                    print('push state: before check effect owner')
                    if self.effectOwner == PlayerType.PLAYER:
                        print('enemy is pushed')
                        if self.selectPushTile>=0 and self.effect.maxRange>0:
                            if not self.field[self.availablePushTile[self.selectPushTile]].is_occupied():
                                self.enemy.move_to(self.field[self.availablePushTile[self.selectPushTile]], self.field)
                                print(f"push target to {self.availablePushTile[self.selectPushTile]}")
                            else:
                                print("can not push, there is an entity of that tile")
                        else:
                            print("there is no push happen")
                    else:
                        print("player is pushed")
                        if self.selectPushTile>=0 and self.effect.maxRange>0:
                            if not self.field[self.availablePushTile[self.selectPushTile]].is_occupied():
                                self.player.move_to(self.field[self.availablePushTile[self.selectPushTile]], self.field)
                                print(f"push target to {self.availablePushTile[self.selectPushTile]}")
                            else:
                                print("can not push, there is an entity of that tile")
                        else:
                            print("there is no push happen")
                    print('push state: after check effect owner')
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

        for tile in self.field:
            if tile.second_entity:
                tile.second_entity.update(dt)
            elif tile.is_occupied() and tile.entity.type == None:
                tile.entity.update(dt)

        self.remove_timeout_entity()
        
    def render(self, screen):
        RenderTurn(screen, 'SelectPushState', self.turn, self.currentTurnOwner)
        RenderEntityStats(screen, self.player, self.enemy)
        RenderSelectedCard(screen, self.player.selectedCard, self.enemy.selectedCard)
        RenderDescription(screen, f"Current Action: {self.effect.type}", f"Owner: {self.effectOwner.value}")
        RenderFieldSelection(screen, self.field, self.availablePushTile, self.selectPushTile, self.effectOwner)
        

        