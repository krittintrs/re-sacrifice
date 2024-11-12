from src.battleSystem.Buff import Buff
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

        self.availableAttackTile = []

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
                self.availableAttackTile.append(i)
        
        for j in range(self.rightMinTileIndex, self.rightMaxTileIndex+1):
            if not self.rightSkip:
                self.availableAttackTile.append(j)
        
        self.availableAttackTile = list( dict.fromkeys(self.availableAttackTile) )

        print('\n!!!! SelectAttackState !!!!')
        print(f'Owner: {self.effectOwner}')
        print(f'Effect: {self.effect.type} ({self.effect.minRange} - {self.effect.maxRange})')

        if self.effectOwner == PlayerType.ENEMY:
            for index in range(len(self.availableAttackTile)):
                if self.field[self.availableAttackTile[index]].is_occupied():
                    if self.field[self.availableAttackTile[index]].entity == self.player:
                        self.selectAttackTile = index

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
                if event.key == pygame.K_LEFT and self.selectAttackTile>=0:
                    if self.effectOwner == PlayerType.PLAYER:
                        self.selectAttackTile = self.selectAttackTile - 1
                        if self.selectAttackTile < 0:
                            self.selectAttackTile = len(self.availableAttackTile) - 1
                if event.key == pygame.K_RIGHT and self.selectAttackTile>=0:
                    if self.effectOwner == PlayerType.PLAYER:
                        self.selectAttackTile = self.selectAttackTile + 1
                        if self.selectAttackTile > len(self.availableAttackTile) - 1:
                            self.selectAttackTile = 0
                if event.key == pygame.K_RETURN:
                    if self.selectAttackTile>=0 and self.effect.maxRange>0:
                        attacking_field = self.field[self.availableAttackTile[self.selectAttackTile]]
                        defender = attacking_field.entity
                        # ATTACK
                        if attacking_field.is_occupied():
                            # RENDER ATTACKER ANIMATION
                            if self.effectOwner == PlayerType.PLAYER:
                                self.player.ChangeAnimation("multi_attack")
                                attacker = self.player
                            elif self.effectOwner == PlayerType.ENEMY:
                                self.enemy.ChangeAnimation("attack")
                                attacker = self.enemy
                            
                            # Damage Calculation
                            if self.effect.type == EffectType.TRUE_DAMAGE:
                                damage = attacker.attack
                            else:
                                damage = attacker.attack - defender.defense

                            # Check For Evade Buff
                            is_evade = False
                            for buff in defender.buffs:
                                if buff.type == BuffType.EVADE:
                                    is_evade = True
                                    break
                               
                            if damage > 0 and not is_evade:
                                # ATTACK HIT
                                gSounds['attack'].play()
                                defender.health -= damage
                                defender.stunt = True
                                print(f'{defender} takes {damage} damage')
                                # RENDER DEFENDER ANIMATION
                                if self.effectOwner == PlayerType.PLAYER:
                                    self.enemy.ChangeAnimation("death")
                                elif self.effectOwner == PlayerType.ENEMY:
                                    self.player.ChangeAnimation("knockdown")
                                # APPLY BUFF
                                if self.effect.type == EffectType.ATTACK_SELF_BUFF:
                                    buff = self.getBuffFromEffect(self.effect)
                                    attacker.add_buff(buff)
                                elif self.effect.type == EffectType.ATTACK_OPPO_BUFF:
                                    buff = self.getBuffFromEffect(self.effect)
                                    defender.add_buff(buff)
                            else:
                                # ATTACK BLOCK
                                gSounds['block'].play()
                                print(f'{defender} takes no damage')
                            defender.print_stats()
                        elif attacking_field.second_entity:
                            if attacking_field.second_entity.side != self.effectOwner:
                                attacking_field.second_entity.take_damage(attacker.attack)
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
        RenderTurn(screen, 'SelectAttackState', self.turn, self.currentTurnOwner)
        RenderEntityStats(screen, self.player, self.enemy)
        RenderSelectedCard(screen, self.player.selectedCard, self.enemy.selectedCard)
        RenderDescription(screen, f"Current Action: {self.effect.type}", f"Owner: {self.effectOwner.value}")
        RenderFieldSelection(screen, self.field, self.availableAttackTile, self.selectAttackTile, self.effectOwner)
        