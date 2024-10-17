from src.states.BaseState import BaseState
from src.dependency import *
from src.constants import *
from src.cardSystem.Card import Card
from src.cardSystem.Entity import Entity
from src.cardSystem.Deck import Deck
import pygame
import sys

import random


class BattlePreparationState(BaseState):
    def __init__(self):
        super(BattlePreparationState, self).__init__()
        self.menu = ["Start Battle", "Edit deck"]
        self.selectIndex = 0
        self.cards = [] # card on hand
        # mock deck
        self.deck = Deck()
        for card in card_dict.values():
            self.deck.addCard(card)

    def Exit(self):
        pass

    def Enter(self, param):
        if param:
            self.deck = param['deck']
        else:
            self.deck = Deck()
            for card in card_dict.values():
                self.deck.addCard(card)

    def update(self, dt, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.selectIndex = (self.selectIndex + 1)%2
                if event.key == pygame.K_LEFT:
                    self.selectIndex = (self.selectIndex - 1)%2
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_RETURN:
                    if self.selectIndex == 0:
                        self.deck.shuffle()
                        for i in range(5):
                            self.cards.append(self.deck.draw(1)[0])
                        g_state_manager.Change("battleInitial", {
                            'deck': self.deck,
                            'cards': self.cards,
                        })
                    else:
                        g_state_manager.Change("deckBuilding", {
                            'deck': self.deck,
                        })


    def render(self, screen):
        # Title
        screen.blit(pygame.font.Font(None, 36).render("Cards:    Press Enter to select", True, (255, 255, 255)), (10, SCREEN_HEIGHT - HUD_HEIGHT + 10))
        for idx, option in enumerate(self.menu):
            if idx == self.selectIndex:
                screen.blit(pygame.font.Font(None, 48).render(">" + option, True, (255,255,255)), (SCREEN_WIDTH/2 - 400 + idx*400, SCREEN_HEIGHT - HUD_HEIGHT + 100))
            else:
                screen.blit(pygame.font.Font(None, 24).render(option, True, (255,255,255)), (SCREEN_WIDTH/2 - 400 + idx*400, SCREEN_HEIGHT - HUD_HEIGHT + 100))
    
        # Mockup render cards
        for order, card in enumerate(self.cards):
            c = Card("card", "description","image", 1 ,1 ,1 ,1 )
            c.render(screen, order)
            
