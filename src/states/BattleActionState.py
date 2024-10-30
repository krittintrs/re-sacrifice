from src.states.BaseState import BaseState
from src.dependency import *
from src.constants import *
from src.battleSystem.Buff import Buff
from src.battleSystem.Effect import Effect
from src.battleSystem.battleEntity.Entity import * 
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

        print(">>>>>> Enter BattleActionState <<<<<<")
        self.player = params['player']
        self.enemy = params['enemy']
        self.field = params['field']
        self.turn = params['turn']
        self.currentTurnOwner = params['currentTurnOwner']  

        # mock card
        #################################
        card = self.player.selectedCard
        print('selected card: ', card.name)
        card.mainEffect.append(Effect("attack", card.range_start, card.range_end))
        # print(card.mainEffect[0].type)
        # print(len(card.beforeEffect))
        # print(len(card.mainEffect))
        # print(len(card.afterEffect))
        # card.beforeEffect = [Effect(EffectType.MOVE, card.range_start, card.range_end)]
        # card.mainEffect = [Effect(EffectType.ATTACK, card.range_start, card.range_end)]
        # card.afterEffect = [Effect(EffectType.SELF_BUFF, card.range_start, card.range_end)]

        # mock player
        # self.player.move_to(self.field[2], self.field)
        
        # mock enemy
        #################################
        new_card = self.enemy.cardsOnHand[0]
        new_card.mainEffect.append(Effect("attack", new_card.range_start, new_card.range_end))
        # new_card.beforeEffect = [Effect(EffectType.MOVE, new_card.range_start, new_card.range_end)]
        # new_card.mainEffect = [Effect(EffectType.ATTACK, new_card.range_start, new_card.range_end)]
        # new_card.afterEffect = [Effect(EffectType.RANGE_BUFF, new_card.range_start, new_card.range_end)]
        self.enemy.select_card(new_card)
        # self.enemy.move_to(self.field[7],self.field)

        # apply existing buff
        self.player.apply_existing_buffs()
        self.enemy.apply_existing_buffs()

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

        if self.player.speed > self.enemy.speed or (self.player.speed == self.enemy.speed and self.currentTurnOwner == PlayerType.PLAYER):
            self.appendEffects(self.player, PlayerType.PLAYER)
            self.appendEffects(self.enemy, PlayerType.ENEMY)

        elif self.player.speed < self.enemy.speed or (self.player.speed == self.enemy.speed and self.currentTurnOwner == PlayerType.ENEMY):
            self.appendEffects(self.enemy, PlayerType.ENEMY)
            self.appendEffects(self.player, PlayerType.PLAYER)

        for card in self.player.cardsOnHand:
            print(f'Player\'s Hand Card: {card.name}, isSelected: {card.isSelected}')

        g_state_manager.Change(BattleState.RESOLVE_PHASE, {
            'player': self.player,
            'enemy': self.enemy,
            'field': self.field,
            'turn': self.turn,
            'currentTurnOwner': self.currentTurnOwner,
            'effectOrder': self.effectOrder
        })

    def appendEffects(self, entity, entityType):
        for beforeEffect in entity.selectedCard.beforeEffect:
            self.effectOrder["before"].append([beforeEffect, entityType])
        for mainEffect in entity.selectedCard.mainEffect:
            self.effectOrder["main"].append([mainEffect, entityType])
        for afterEffect in entity.selectedCard.afterEffect:
            self.effectOrder["after"].append([afterEffect, entityType])

    def render(self, screen):  
        # Turn
        screen.blit(pygame.font.Font(None, 36).render(f"Turn {self.turn}", True, (0, 0, 0)), (10, 10))   

        # Render cards on player's hand
        for order, card in enumerate(self.player.cardsOnHand):
            card.render(screen, order)

        # Render field
        for fieldTile in self.field:
            fieldTile.render(screen, len(self.field))