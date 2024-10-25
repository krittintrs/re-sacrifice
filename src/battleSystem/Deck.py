import copy
import random
import pygame

class Deck:
    def __init__(self):
        self.card_deck = []
        self.discard_pile = []
    
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

    def render(self, screen):
        # Draw the deck
        pygame.draw.rect(screen, (0, 0, 0), (10, 10, 100, 150), 1)

    def update(self, dt, events):
        pass