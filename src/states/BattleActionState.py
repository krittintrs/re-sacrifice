import random
from src.states.BaseState import BaseState
from src.dependency import *
from src.constants import *
from src.BattlePause import *
from src.Render import *
import pygame
import sys

class BattleActionState(BaseState):
    def __init__(self):
        super(BattleActionState, self).__init__()
        self.effectOrder = {"before": [], "main": [], "after":[]}
        self.pauseHandler = BattlePauseHandler()

    def Enter(self, params):
        print("\n>>>>>> Enter BattleActionState <<<<<<")
        self.params = params
        battle_param = self.params['battleSystem']
        self.player = battle_param['player']
        self.enemy = battle_param['enemy']
        self.field = battle_param['field']
        self.turn = battle_param['turn']
        self.currentTurnOwner = battle_param['currentTurnOwner']  

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
            self.enemy.selectedCard.speed += 1
            self.ditto = True
        
        # apply buff to all cards on hand
        self.player.apply_buffs_to_cardsOnHand()
        self.enemy.apply_buffs_to_cardsOnHand()

        # display entity stats
        self.player.display_stats()
        self.enemy.display_stats()

        # sort effects
        self.sortEffects()

        self.pauseHandler.reset()

    def Exit(self):
        pass

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
                if event.key == pygame.K_RETURN:
                    # print(self.effectOrder)
                    # if self.effectOrder["main"]:
                    #     for effectDetail in self.effectOrder["main"]:
                    #         print(effectDetail[0].type)
                    self.params['battleSystem'] = {
                        'player': self.player,
                        'enemy': self.enemy,
                        'field': self.field,
                        'turn': self.turn,
                        'currentTurnOwner': self.currentTurnOwner,
                        'effectOrder': self.effectOrder,
                    }
                    g_state_manager.Change(BattleState.RESOLVE_PHASE, self.params)

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
        if self.ditto:
            RenderSelectedCard(screen, self.player.selectedCard, self.reserve_enemy_card)
        else:
            RenderSelectedCard(screen, self.player.selectedCard, self.enemy.selectedCard)
        RenderDescription(screen, "Resolve Action: Press Enter to Confirm")
        
        # Render field
        for fieldTile in self.field:
            fieldTile.render(screen)

        self.pauseHandler.render(screen)