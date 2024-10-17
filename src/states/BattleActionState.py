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

    def Enter(self, param):
        """
        params:
            - player = Player() : player entity
            - enemy = Enemy() : enemy entity
            - field = list[fieldTile] : list of fieldTile objects (each fieldTile is one squre)
            - dice = int : dice result 
            - selected_card_index = int : index of selected card in cards
        """

        print("enter action state")
        self.player = param['player']
        self.enemy = param['enemy']
        self.field = param['field']
        self.turn = param['turn']
        self.currentTurnOwner = param['currentTurnOwner']  
        self.selected_card_index = param['selected_card_index']

        # mock card
        card = self.player.cardsOnHand[self.selected_card_index]
        print('selected card: ', card.name)
        card.beforeEffect = [Effect("attack", 0, card.range)]
        card.mainEffect = [Effect("attack", 0, card.range)]
        card.afterEffect = [Effect("attack", 0, card.range)]

        # mock player
        self.player.select_card(card)
        self.player.move_to(self.field[1], self.field)
        
        # mock enemy
        card.beforeEffect = [Effect("move", 0, card.range)]
        card.mainEffect = [Effect("move", 0, card.range)]
        card.afterEffect = [Effect("move", 0, card.range)]
        self.enemy.select_card(card)
        self.enemy.move_to(self.field[7],self.field)

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

        if self.player.get_speed() > self.enemy.get_speed() or (self.player.get_speed() == self.enemy.get_speed() and self.currentTurnOwner == TurnOwner.PLAYER):
            for beforeEffect in self.player.selected_card.beforeEffect:
                self.effectOrder["before"].append(["player",beforeEffect])
            for mainEffect in self.player.selected_card.mainEffect:
                self.effectOrder["main"].append(["player",mainEffect])
            for afterEffect in self.player.selected_card.afterEffect:
                self.effectOrder["after"].append(["player",afterEffect])

            for beforeEffect in self.enemy.selected_card.beforeEffect:
                self.effectOrder["before"].append(["enemy",beforeEffect])
            for mainEffect in self.enemy.selected_card.mainEffect:
                self.effectOrder["main"].append(["enemy",mainEffect])
            for afterEffect in self.enemy.selected_card.afterEffect:
                self.effectOrder["after"].append(["enemy",afterEffect])

        elif self.player.get_speed() < self.enemy.get_speed() or (self.player.get_speed() == self.enemy.get_speed() and self.currentTurnOwner == TurnOwner.ENEMY):
            for beforeEffect in self.enemy.selected_card.beforeEffect:
                self.effectOrder["before"].append(["enemy",beforeEffect])
            for mainEffect in self.enemy.selected_card.mainEffect:
                self.effectOrder["main"].append(["enemy",mainEffect])
            for afterEffect in self.enemy.selected_card.afterEffect:
                self.effectOrder["after"].append(["enemy",afterEffect])
            
            for beforeEffect in self.player.selected_card.beforeEffect:
                self.effectOrder["before"].append(["player",beforeEffect])
            for mainEffect in self.player.selected_card.mainEffect:
                self.effectOrder["main"].append(["player",mainEffect])
            for afterEffect in self.player.selected_card.afterEffect:
                self.effectOrder["after"].append(["player",afterEffect])

    def render(self, screen):  
        # Render cards on player's hand
        for order, card in enumerate(self.player.cardsOnHand):
            card.render(screen, order)
            card.render_selected(screen, self.selected_card_index)

        # Render field
        for fieldTile in self.field:
            fieldTile.render(screen, len(self.field))