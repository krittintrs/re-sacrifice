from src.states.BaseState import BaseState
from src.dependency import *
from src.constants import *
from src.Render import *
import pygame
import sys

class SelectAttackState(BaseState):
    def __init__(self):
        super(SelectAttackState, self).__init__()

    def Enter(self, params):
        self.player = params['player']
        self.enemy = params['enemy']
        self.field = params['field']
        self.turn = params['turn']
        self.currentTurnOwner = params['currentTurnOwner']  
        self.effectOrder = params['effectOrder']
        self.effect = params['effect']
        self.effectOwner = params['effectOwner']
        self.choosing = False

        self.leftSkip = False
        self.rightSkip = False

        self.avilableAttackTile = []

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
        
        self.selectAttackTile = 0

        if self.rightSkip and self.leftSkip:
                self.selectAttackTile = -1

        for i in range(self.leftMaxTileIndex, self.leftMinTileIndex+1):
            if not self.leftSkip:
                self.avilableAttackTile.append(i)
        
        for j in range(self.rightMinTileIndex, self.rightMaxTileIndex+1):
            if not self.rightSkip:
                self.avilableAttackTile.append(j)
        
        self.avilableAttackTile = list( dict.fromkeys(self.avilableAttackTile) )

        print('\n!!!! SelectAttackState !!!!')
        print(f'Owner: {self.effectOwner}')
        print(f'Effect: {self.effect.type} ({self.effect.minRange} - {self.effect.maxRange})')

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
                if event.key == pygame.K_LEFT and self.selectAttackTile>=0:
                    if self.effectOwner == PlayerType.PLAYER:
                        self.selectAttackTile = self.selectAttackTile - 1
                        if self.selectAttackTile < 0:
                            self.selectAttackTile = len(self.avilableAttackTile) - 1
                if event.key == pygame.K_RIGHT and self.selectAttackTile>=0:
                    if self.effectOwner == PlayerType.PLAYER:
                        self.selectAttackTile = self.selectAttackTile + 1
                        if self.selectAttackTile > len(self.avilableAttackTile) - 1:
                            self.selectAttackTile = 0
                if event.key == pygame.K_RETURN:
                    if self.effectOwner == PlayerType.PLAYER:
                        if self.selectAttackTile>=0 and self.effect.maxRange>0:
                            if self.field[self.avilableAttackTile[self.selectAttackTile]].is_occupied():
                                self.player.ChangeAnimation("multi_attack")
                                self.enemy.ChangeAnimation("death")
                                damage = self.player.attack - self.field[self.avilableAttackTile[self.selectAttackTile]].entity.defense
                                if damage > 0:
                                    gSounds['attack'].play()
                                    self.field[self.avilableAttackTile[self.selectAttackTile]].entity.health -= damage
                                    self.field[self.avilableAttackTile[self.selectAttackTile]].entity.stunt = True
                                    print(f'{self.field[self.avilableAttackTile[self.selectAttackTile]].entity} takes {damage} damage')
                                else:
                                    gSounds['block'].play()
                                    print(f'{self.field[self.avilableAttackTile[self.selectAttackTile]].entity} takes no damage')
                                self.field[self.avilableAttackTile[self.selectAttackTile]].entity.print_stats()
                            else:
                                print("no entity on the targeted tile")
                        else:
                            print("there is no attack happen")
                    
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
        RenderTurn(screen, 'SelectAttackState', self.turn, self.currentTurnOwner)
        RenderEntityStats(screen, self.player, self.enemy)
        RenderSelectedCard(screen, self.player.selectedCard, self.enemy.selectedCard)

        # Render field
        for fieldTile in self.field:               
            # Render the range of the attack

            if fieldTile.index in set(self.avilableAttackTile):
                fieldTile.color = (255,0,0)
            else:
                fieldTile.color = (0,0,0)
            if self.selectAttackTile>=0:
                if fieldTile.index == self.avilableAttackTile[self.selectAttackTile]:
                    fieldTile.color = (255,0,255)
                    fieldTile.solid = 0
                
            fieldTile.render(screen)
            fieldTile.color = (0,0,0)
            fieldTile.solid = 1