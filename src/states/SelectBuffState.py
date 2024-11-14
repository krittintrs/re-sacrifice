from src.states.BaseState import BaseState
from src.dependency import *
from src.constants import *
from src.Render import *
from src.battleSystem.Buff import Buff
import pygame
import sys

class SelectBuffState(BaseState):
    def __init__(self):
        super(SelectBuffState, self).__init__()

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

        self.availableBuffTile = []

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
                self.availableBuffTile.append(i)
        
        for j in range(self.rightMinTileIndex, self.rightMaxTileIndex+1):
            if not self.rightSkip:
                self.availableBuffTile.append(j)
        
        self.availableBuffTile = list( dict.fromkeys(self.availableBuffTile) )

        print('\n!!!! SelectBuffState !!!!')
        print(f'Owner: {self.effectOwner}')
        print(f'Effect: {self.effect.type} ({self.effect.minRange} - {self.effect.maxRange})')

        if self.effectOwner == PlayerType.ENEMY:
            for index in range(len(self.availableBuffTile)):
                if self.field[self.availableBuffTile[index]].is_occupied():
                    if self.field[self.availableBuffTile[index]].entity == self.player:
                        self.selectBuffTile = index

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
                if event.key == pygame.K_LEFT and self.selectBuffTile>=0:
                    if self.effectOwner == PlayerType.PLAYER:
                        self.selectBuffTile = self.selectBuffTile - 1
                        if self.selectBuffTile < 0:
                            self.selectBuffTile = len(self.availableBuffTile) - 1
                if event.key == pygame.K_RIGHT and self.selectBuffTile>=0:
                    if self.effectOwner == PlayerType.PLAYER:
                        self.selectBuffTile = self.selectBuffTile + 1
                        if self.selectBuffTile > len(self.availableBuffTile) - 1:
                            self.selectBuffTile = 0
                if event.key == pygame.K_RETURN:
                    if self.effectOwner == PlayerType.PLAYER:
                        if self.selectBuffTile>=0 and self.effect.maxRange>0:
                            if self.field[self.availableBuffTile[self.selectBuffTile]].is_occupied():
                                debuff = self.getBuffFromEffect(self.effect)
                                self.enemy.add_buff(debuff)
                                print(f"apply buff {debuff} to enemy")
                            else:
                                print("no entity on the targeted tile")
                        else:
                            print("there is no buff happen")
                    if self.effectOwner == PlayerType.ENEMY:
                        if self.selectBuffTile>=0 and self.effect.maxRange>0:
                            if self.field[self.availableBuffTile[self.selectBuffTile]].is_occupied():
                                debuff = self.getBuffFromEffect(self.effect)
                                self.player.add_buff(debuff)
                                print(f"apply buff {debuff} to player")
                            else:
                                print("no entity on the targeted tile")
                        else:
                            print("there is no buff happen")

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

    def getBuffFromEffect(self, effect):
        if effect.buffName:
            buff = Buff(CARD_BUFF[effect.buffName])
            return buff
        else:
            print(f'Buff not found: {effect.buffName}')
            return False
          
    def render(self, screen):
        RenderTurn(screen, 'SelectBuffState', self.turn, self.currentTurnOwner)
        RenderEntityStats(screen, self.player, self.enemy)
        RenderSelectedCard(screen, self.player.selectedCard, self.enemy.selectedCard)
        RenderDescription(screen, f"Current Action: {self.effect.type}", f"Owner: {self.effectOwner.value}")
        RenderFieldSelection(screen, self.field, self.availableBuffTile, self.selectBuffTile, self.effectOwner)
        

        