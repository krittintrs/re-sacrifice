from src.states.BaseState import BaseState
from src.dependency import *
from src.constants import *
from src.cardSystem.Buff import Buff
from src.cardSystem.Effect import Effect
from src.cardSystem.Entity import * 
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
            - dice = int : dice result 
            - selected_card_index = int : index of selected card in cards
            - currentTurnOwner = TurnOwner : current turn owner
            - turn = int : current turn
        """

        print(">>>>>> Enter BattleActionState <<<<<<")
        self.player = params['player']
        self.enemy = params['enemy']
        self.field = params['field']
        self.turn = params['turn']
        self.currentTurnOwner = params['currentTurnOwner']  
        self.selected_card_index = params['selected_card_index']

        # mock card
        card = self.player.cardsOnHand[self.selected_card_index]
        print('selected card: ', card.name)
        card.beforeEffect = [Effect("attack", 0, card.range)]
        card.mainEffect = [Effect("attack", 0, card.range)]
        card.afterEffect = [Effect("attack", 0, card.range)]

        # mock player
        self.player.select_card(card)
        self.player.move_to(self.field[2], self.field)
        
        # mock enemy
        card.beforeEffect = [Effect("move", 0, card.range)]
        card.mainEffect = [Effect("move", 0, card.range)]
        card.afterEffect = [Effect("move", 0, card.range)]
        self.enemy.select_card(card)
        self.enemy.move_to(self.field[7],self.field)

        # apply buff
        self.player.apply_buff()
        self.enemy.apply_buff()

        for fieldTile in self.field:
            print(f'FieldTile {fieldTile.index} is occupied by {fieldTile.entity.name if fieldTile.entity else None}')

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
                if event.key == pygame.K_RETURN:
                    pass

        if self.player.speed > self.enemy.speed or (self.player.speed == self.enemy.speed and self.currentTurnOwner == PlayerType.PLAYER):
            self.appendEffects(self.player, PlayerType.PLAYER)
            self.appendEffects(self.enemy, PlayerType.ENEMY)

        elif self.player.speed < self.enemy.speed or (self.player.speed == self.enemy.speed and self.currentTurnOwner == PlayerType.ENEMY):
            self.appendEffects(self.enemy, PlayerType.ENEMY)
            self.appendEffects(self.player, PlayerType.PLAYER)

        g_state_manager.Change(BattleState.RESOLVE_PHASE, {
            'player': self.player,
            'enemy': self.enemy,
            'field': self.field,
            'turn': self.turn,
            'currentTurnOwner': self.currentTurnOwner,
            'selected_card_index': self.selected_card_index,
            'effectOrder': self.effectOrder
        })

    def appendEffects(self, entity, entityType):
        for beforeEffect in entity.selected_card.beforeEffect:
            self.effectOrder["before"].append([entityType, beforeEffect])
        for mainEffect in entity.selected_card.mainEffect:
            self.effectOrder["main"].append([entityType, mainEffect])
        for afterEffect in entity.selected_card.afterEffect:
            self.effectOrder["after"].append([entityType, afterEffect])

    def render(self, screen):  
        # Render cards on player's hand
        for order, card in enumerate(self.player.cardsOnHand):
            card.render(screen, order)
            card.render_selected(screen, self.selected_card_index)

        # Render field
        for fieldTile in self.field:
            fieldTile.render(screen, len(self.field))