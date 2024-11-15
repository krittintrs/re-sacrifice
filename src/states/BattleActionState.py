import random
from src.states.BaseState import BaseState
from src.dependency import *
from src.constants import *
from src.battleSystem.battleEntity.Entity import * 
from src.Render import *
import pygame
import sys

class BattleActionState(BaseState):
    def __init__(self):
        super(BattleActionState, self).__init__()
        self.effectOrder = {"before": [], "main": [], "after":[]}

    def Enter(self, params):
        """
        params:
            - player = Player() : player entity
            - enemy = Enemy() : enemy entity
            - field = list[fieldTile] : list of fieldTile objects (each fieldTile is one squre)
            - turn = int : current turn
            - currentTurnOwner = TurnOwner : current turn owner
        """

        print("\n>>>>>> Enter BattleActionState <<<<<<")
        self.player = params['player']
        self.enemy = params['enemy']
        self.field = params['field']
        self.turn = params['turn']
        self.currentTurnOwner = params['currentTurnOwner']  

        # player
        player_selected_card = self.player.selectedCard
        player_selected_card.print_effects()

        # enemy
        enemy_selected_Card_index = self.enemy.cardDecision(self.player)
        enemy_selected_card = self.enemy.cardsOnHand[enemy_selected_Card_index] #for normal goblin it's just random
        self.enemy.select_card(enemy_selected_card)
        enemy_selected_card.print_effects()
        self.ditto = False

        if self.enemy.selectedCard.name == "Ditto":
            self.reserve_enemy_card = self.enemy.selectedCard
            self.enemy.selectedCard = self.player.selectedCard
            self.ditto = True
        
        # apply buff to all cards on hand
        self.player.apply_buffs_to_cardsOnHand()
        self.enemy.apply_buffs_to_cardsOnHand()

        # display entity stats
        self.player.display_stats()
        self.enemy.display_stats()

        if self.ditto:
            self.enemy.speed += 1

        # sort effects
        self.sortEffects()

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
                if event.key == pygame.K_RETURN:
                    g_state_manager.Change(BattleState.RESOLVE_PHASE, {
                        'player': self.player,
                        'enemy': self.enemy,
                        'field': self.field,
                        'turn': self.turn,
                        'currentTurnOwner': self.currentTurnOwner,
                        'effectOrder': self.effectOrder,
                    })

        # Update buff
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

    def remove_timeout_entity(self):
        for tile in self.field:
            if tile.is_second_entity():
                if tile.second_entity.duration == 0:
                    print("remove second entity for timeout ", tile.index)
                    tile.remove_second_entity()
    
    def sortEffects(self):
        playerSpeed = self.player.selectedCard.buffed_speed
        enemySpeed = self.enemy.selectedCard.buffed_speed

        if self.ditto:
            enemySpeed = self.player.selectedCard.buffed_speed + 1

        if playerSpeed > enemySpeed or (playerSpeed == enemySpeed and self.currentTurnOwner == PlayerType.PLAYER):
            self.appendEffects(self.player, PlayerType.PLAYER)
            self.appendEffects(self.enemy, PlayerType.ENEMY)

        elif playerSpeed < enemySpeed or (playerSpeed == enemySpeed and self.currentTurnOwner == PlayerType.ENEMY):
            self.appendEffects(self.enemy, PlayerType.ENEMY)
            self.appendEffects(self.player, PlayerType.PLAYER)

    def appendEffects(self, entity, entityType):
        for beforeEffect in entity.selectedCard.beforeEffect:
            self.effectOrder["before"].append([beforeEffect, entityType])
        for mainEffect in entity.selectedCard.mainEffect:
            self.effectOrder["main"].append([mainEffect, entityType])
        for afterEffect in entity.selectedCard.afterEffect:
            self.effectOrder["after"].append([afterEffect, entityType])

    def render(self, screen):  
        RenderTurn(screen, 'battleAction', self.turn, self.currentTurnOwner)
        RenderEntityStats(screen, self.player, self.enemy)
        RenderSelectedCard(screen, self.player.selectedCard, self.enemy.selectedCard)
        RenderDescription(screen, "Resolve Action: Press Enter to Confirm")
        
        # Render field
        for fieldTile in self.field:
            fieldTile.render(screen)