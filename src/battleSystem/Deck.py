import copy
import random
import pygame
from src.battleSystem.Card import Card
from src.dependency import *

class Deck:
    def __init__(self):
        self.card_deck = []
        self.discard_pile = []
        self.inventory = []

    def read_conf(self, conf = DECK_DEFS["default"]):
        print(f"Reading deck conf: {conf}")
        self.card_deck = []
        for card_info in conf.card_dict:
            for i in range(card_info["quantity"]):
                card = Card()
                card.read_conf(CARD_DEFS[card_info["name"]])
                self.card_deck.append(card)

    
    def draw(self, number):
        drawn_cards = self.card_deck[:number]
        self.card_deck = self.card_deck[number:]
        return drawn_cards
    
    def shuffle(self):
        random.shuffle(self.card_deck)

    def reset(self):
        self.card_deck = self.card_deck + self.discard_pile
        self.discard_pile = []
        self.shuffle()

    def addCard(self, card):
        self.card_deck.append(card)

    def removeCard(self, card):
        if card in self.card_deck:
            self.card_deck.remove(card)
        elif card in self.discard_pile:
            self.discard_pile.remove(card)
        else:
            print("Card not found in deck or discard pile")

    def isCardLimitReach(self):
        if len(self.card_deck) >= 30:
            return True
        else:
            return False
        
    def isCardMinimumReach(self):
        if len(self.card_deck) < 20:
            return False
        else:
            return True
        
    def isCardDuplicateWithinLimit(self):
        dup = {}
        for card in self.card_deck:
            if card.name in dup:
                dup[card.name] += 1
            else:
                dup[card.name] = 1
        for i in list(dup.values()):
            if i > 3:
                return False
        return True
    
    
    # Inventory methods
    def addCardInventory(self, card_name):
        card = Card()
        card.read_conf(CARD_DEFS[card_name])
        self.inventory.append(card)

    def removeCardInventory(self, card: Card):
        if card in self.inventory:
            self.inventory.remove(card)
        else:
            print("Card is not in inventory")

    def readInventoryConf(self, conf = DECK_DEFS["default_inventory"]):
        """
        Note that it read from the source as deck (DECK_DEFS)
        """
        self.inventory = []
        for card_info in conf.card_dict:
            for i in range(card_info["quantity"]):
                card = Card()
                card.read_conf(CARD_DEFS[card_info["name"]])
                self.inventory.append(card)

    


    def render(self, screen):
        # Draw the deck
        pygame.draw.rect(screen, (0, 0, 0), (10, 10, 100, 150), 1)

    def update(self, dt, events):
        pass