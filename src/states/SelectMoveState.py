import random
from src.states.BaseState import BaseState
from src.dependency import *
from src.constants import *
from src.BattlePause import *
from src.Render import *
import pygame
import sys
import time

class SelectMoveState(BaseState):
    def __init__(self):
        super(SelectMoveState, self).__init__()
        self.pauseHandler = BattlePauseHandler()

    def Enter(self, params):
        self.params = params
        battle_param = self.params['battleSystem']
        self.player = battle_param['player']
        self.enemy = battle_param['enemy']
        self.field = battle_param['field']
        self.turn = battle_param['turn']
        self.currentTurnOwner = battle_param['currentTurnOwner']  
        self.effectOrder = battle_param['effectOrder']
        self.effect = battle_param['effect']
        self.effectOwner = battle_param['effectOwner']
        
        self.leftSkip = False
        self.rightSkip = False

        self.availableMoveTile = []

        if self.effectOwner == PlayerType.PLAYER:
            for buff in self.player.buffs:
                if buff.type == BuffType.STOP_MOVEMENT:
                    print("can not move due to debuff")
                    self.player.ChangeAnimation('knock_down')
                    time.sleep(1)
                    # self.leftSkip = True
                    # self.rightSkip = True
                    self.params['battleSystem'] = {
                        'player': self.player,
                        'enemy': self.enemy,
                        'field': self.field,
                        'turn': self.turn,
                        'currentTurnOwner': self.currentTurnOwner,
                        'effectOrder': self.effectOrder
                    }
                    g_state_manager.Change(BattleState.RESOLVE_PHASE, self.params)
            startIndex = self.player.fieldTile_index
            self.leftMinTileIndex = self.player.fieldTile_index - self.effect.minRange
            self.leftMaxTileIndex = self.player.fieldTile_index - self.effect.maxRange
            self.rightMinTileIndex = self.player.fieldTile_index + self.effect.minRange
            self.rightMaxTileIndex = self.player.fieldTile_index + self.effect.maxRange
            print("should still run this code though")
        elif self.effectOwner == PlayerType.ENEMY:
            for buff in self.enemy.buffs:
                if buff.type == BuffType.STOP_MOVEMENT:
                    print("can not move due to debuff")
                    self.enemy.ChangeAnimation('death')
                    time.sleep(1)
                    # self.leftSkip = True
                    # self.rightSkip = True
                    self.params['battleSystem'] = {
                        'player': self.player,
                        'enemy': self.enemy,
                        'field': self.field,
                        'turn': self.turn,
                        'currentTurnOwner': self.currentTurnOwner,
                        'effectOrder': self.effectOrder
                    }
                    g_state_manager.Change(BattleState.RESOLVE_PHASE, self.params)
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
            if tile.is_occupied():
                self.availableMoveTile.remove(index)

        
        self.availableMoveTile = list( dict.fromkeys(self.availableMoveTile) )
        
        print('\n!!!! SelectMoveState !!!!')
        print(f'Owner: {self.effectOwner}')
        print(f'Effect: {self.effect.type} ({self.effect.minRange} - {self.effect.maxRange})')
        print(f'SelectMoveTile: {self.selectMoveTile}')

        if self.effectOwner == PlayerType.ENEMY:
            self.selectMoveTile = self.enemy.moveDecision(self.availableMoveTile, self.field, self.player, self.currentTurnOwner)
        
        # apply buff to all cards on hand
        self.player.apply_buffs_to_cardsOnHand()
        self.enemy.apply_buffs_to_cardsOnHand()

        # display entity stats
        self.player.display_stats()
        self.enemy.display_stats()

        self.pauseHandler.reset()

    def Exit(self):
        pass

    def check_collision(self):
        selected_field = self.field[self.availableMoveTile[self.selectMoveTile]]
        if selected_field.is_second_entity():
            if self.effectOwner == PlayerType.PLAYER:
                selected_field.second_entity.collide(self.player)
            elif self.effectOwner == PlayerType.ENEMY:
                selected_field.second_entity.collide(self.enemy)

    def remove_timeout_entity(self):
        for tile in self.field:
            if tile.is_second_entity():
                if tile.second_entity.duration == 0:
                    print("remove second entity for timeout ", tile.index)
                    tile.remove_second_entity()

    def update(self, dt, events):
        if self.pauseHandler.is_paused():
            self.pauseHandler.update(dt, events, self.params)
            return
        
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.pauseHandler.pause_game()
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
                                self.player.move_to(self.field[self.availableMoveTile[self.selectMoveTile]], self.field, self.check_collision)
                                print(f"{self.effectOwner} move to {self.availableMoveTile[self.selectMoveTile]}")
                            else:
                                print("can not move, there is an entity of that tile")
                        else:
                            print("there is no movement happen")
                    else:
                        print("enemy movement")
                        if self.selectMoveTile>=0 and self.effect.maxRange>0:
                            if not selected_field.is_occupied():
                                self.enemy.move_to(self.field[self.availableMoveTile[self.selectMoveTile]], self.field, self.check_collision)
                                print(f"{self.effectOwner} move to {self.availableMoveTile[self.selectMoveTile]}")
                            else:
                                print("can not move, there is an entity of that tile")
                        else:
                            print("there is no movement happen")
                    print('move state: after check effect owner')
                    if self.player.health > 0 and self.enemy.health > 0:
                        self.params['battleSystem'] = {
                            'player': self.player,
                            'enemy': self.enemy,
                            'field': self.field,
                            'turn': self.turn,
                            'currentTurnOwner': self.currentTurnOwner,
                            'effectOrder': self.effectOrder
                        }
                        g_state_manager.Change(BattleState.RESOLVE_PHASE, self.params)
                    else:
                        if self.player.health <= 0:
                            self.winner = PlayerType.ENEMY
                        elif self.enemy.health <= 0:
                            self.winner = PlayerType.PLAYER
                        self.params['battleSystem'] = {
                            'player': self.player,
                            'enemy': self.enemy,
                            'field': self.field,
                            'turn': self.turn,
                            'currentTurnOwner': self.currentTurnOwner,
                            'winner': self.winner
                        }
                        g_state_manager.Change(BattleState.FINISH_PHASE, self.params)

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
        RenderTurn(screen, 'SelectMoveState', self.turn, self.currentTurnOwner)
        RenderEntityStats(screen, self.player, self.enemy)
        RenderSelectedCard(screen, self.player.selectedCard, self.enemy.selectedCard)
        RenderDescription(screen, f"Current Action: {self.effect.type.value}", f"Owner: {self.effectOwner.value}")
        RenderFieldSelection(screen, self.field, self.availableMoveTile, self.selectMoveTile, self.effectOwner)

        self.pauseHandler.render(screen)
        