from src.states.BaseState import BaseState
from src.dependency import *
from src.constants import *
from src.cardSystem.Card import Card
from src.cardSystem.Buff import Buff
from src.cardSystem.Field import Field 
from src.cardSystem.Effect import Effect
from src.cardSystem.Entity import * 
import pygame
import sys

class BattleActionState(BaseState):
    def __init__(self):
        super(BattleActionState, self).__init__()
        self.playerFirst = True
        self.effectOrder = {"before": [], "main": [], "after":[]}

    def Enter(self, params):
        """
        params:
            - cards = list[Card] : list of cards in player hand
            - entities = lsit[Entity] : list of entities in the field
            - fields = list[Field] : list of field objects (each field is one squre)
            - dice = int : dice result 
            - selected_card = int : index of selected card in cards
        """

        print("enter action state")
        self.cards = params['cards']
        self.fields = params['fields']
        self.dice = params['dice']
        self.selected_card = params['selected_card']

        # mock card
        card = self.cards[params['selected_card']]
        card.beforeEffect = [Effect("attack", 0, card.range)]
        card.mainEffect = [Effect("attack", 0, card.range)]
        card.afterEffect = [Effect("attack", 0, card.range)]

        # mock player
        self.fields[4].remove_entity()
        self.player = Player("player")
        self.player.select_card(card)
        self.player.move_to(self.fields[1], self.fields)
        
        # mock enemy
        card.beforeEffect = [Effect("move", 0, card.range)]
        card.mainEffect = [Effect("move", 0, card.range)]
        card.afterEffect = [Effect("move", 0, card.range)]
        self.enemy = Enemy("enemy")
        self.enemy.select_card(card)
        self.enemy.move_to(self.fields[7],self.fields)

        # mock turn
        if "turn" in params: # should be parse from the previous state
            self.turn = params['turn']
        else:
            self.turn = 1
        
        self.dice_buff(self.dice)
    
    # convert dice value to buff
    def dice_buff(self, dice):
        if dice < 4: # 1, 2, 3
            value = [0, 0, 0, 0] # atk, def, spd, range
            value[dice-1] = 1
            if self.turn%2 == 1: # let odd turn be a player turn
                buff = Buff("bonus", 1, value)
                self.player.add_buff(buff)
            else:
                buff = Buff("bonus", 1, value)
                self.enemy.add_buff(buff)
        else:
            return
        
    def get_turn(self):
        if self.turn%2 == 1:
            return "player"
        else:
            return "enemy"

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

        if self.player.get_speed() > self.enemy.get_speed() or (self.player.get_speed() == self.enemy.get_speed() and self.get_turn() == "player"):
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

        elif self.player.get_speed() < self.enemy.get_speed() or (self.player.get_speed() == self.enemy.get_speed() and self.get_turn() == "enemy"):
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
        # render cards
        for order, card in enumerate(self.cards):
            card.render(screen, order)
            card.render_selected(screen, self.selected_card)

        # Render fields
        for field in self.fields:
            field.render(screen, len(self.fields))