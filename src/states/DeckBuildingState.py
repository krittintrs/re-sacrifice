from src.states.BaseState import BaseState
from src.dependency import *
from src.constants import *
import pygame
import sys

class DeckBuildingState(BaseState):

    def __init__(self):
        super(DeckBuildingState, self).__init__()
        self.avaliableCard = []
        self.selectDeck = True
        self.deckIndex = 0
        self.avaliableCardIndex = 0
        self.cardPerRow = 8
        self.avaliableCardSpacing = 10
        self.deckSpacing = 5
        self.selectedCardSpacing = 20

        # mock avaliable card
        for card in card_dic.values():
            self.avaliableCard.append(card)
        

    def Enter(self, params):
        self.deck = params["deck"]

    def Exit(self):
        pass

    def update(self, dt, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    if self.selectDeck:
                        if (self.deckIndex)%self.cardPerRow == (self.cardPerRow - 1) or self.deckIndex == len(self.deck.card_deck)-1 or len(self.deck.card_deck)==0:
                            self.selectDeck = False
                        elif self.deckIndex < len(self.deck.card_deck) -1:
                            self.deckIndex +=1 
                if event.key == pygame.K_LEFT:
                    if self.selectDeck:
                        if self.deckIndex > 0:
                            self.deckIndex -=1
                    else:
                        self.selectDeck = True
                if event.key == pygame.K_DOWN:
                    if self.selectDeck:
                        if self.deckIndex + self.cardPerRow < len(self.deck.card_deck):
                            self.deckIndex += self.cardPerRow
                    else:
                        if self.avaliableCardIndex < len(self.avaliableCard) - 1:
                            self.avaliableCardIndex += 1
                if event.key == pygame.K_UP:
                    if self.selectDeck:
                        if self.deckIndex - self.cardPerRow >= 0:
                            self.deckIndex -= self.cardPerRow
                    else:
                        if self.avaliableCardIndex > 0:
                            self.avaliableCardIndex -= 1
                if event.key == pygame.K_SPACE:
                    if self.selectDeck:
                        if len(self.deck.card_deck)!=0:
                            if self.deckIndex == len(self.deck.card_deck) - 1 and self.deckIndex != 0:
                                self.deckIndex -= 1
                            card = self.deck.card_deck[self.deckIndex]
                            self.avaliableCard.append(card)
                            self.deck.removeCard(card)
                    else:
                        if len(self.avaliableCard)!=0:
                            if self.avaliableCardIndex == len(self.avaliableCard)- 1 and self.avaliableCardIndex != 0:
                                self.avaliableCardIndex -= 1
                            card = self.avaliableCard.pop(self.avaliableCardIndex)
                            self.deck.addCard(card)

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_RETURN:
                    g_state_manager.Change("prepare", {
                        'deck':self.deck,
                    })

    def render(self, screen):
        screen.fill((255,255,255))
        # mock layout
        pygame.draw.rect(screen, (255,255,0), (0,0, SCREEN_WIDTH * 0.25, SCREEN_HEIGHT), 5)
        pygame.draw.rect(screen, (255,0,0), (SCREEN_WIDTH * 0.25,0, SCREEN_WIDTH * 0.75, SCREEN_HEIGHT*0.2), 5)
        pygame.draw.rect(screen, (0,255,0), (SCREEN_WIDTH * 0.25,SCREEN_HEIGHT*0.2, SCREEN_WIDTH * 0.5, SCREEN_HEIGHT*0.8), 5)
        pygame.draw.rect(screen, (0,0,255), (SCREEN_WIDTH * 0.75,SCREEN_HEIGHT*0.2, SCREEN_WIDTH * 0.25, SCREEN_HEIGHT*0.8), 5)

        # render deck
        deckScale = (SCREEN_WIDTH*0.5)/((CARD_WIDTH + self.deckSpacing * 3)*self.cardPerRow)
        for idx, card in enumerate(self.deck.card_deck):
            card.renderPosition(screen, (SCREEN_WIDTH * 0.25 + self.deckSpacing + (CARD_WIDTH*deckScale + self.deckSpacing)*(idx%self.cardPerRow) ,SCREEN_HEIGHT*0.2 + self.deckSpacing+ (CARD_HEIGHT*deckScale + self.deckSpacing)*(idx//self.cardPerRow)),deckScale)
            screen.blit(pygame.font.Font(None, 24).render(card.name, True, (0,0,0)), (SCREEN_WIDTH * 0.25 + self.deckSpacing + (CARD_WIDTH*deckScale + self.deckSpacing)*(idx%self.cardPerRow) ,SCREEN_HEIGHT*0.2 + self.deckSpacing+ (CARD_HEIGHT*deckScale + self.deckSpacing)*(idx//self.cardPerRow)))

        
        # render avaliable cards
        avaliableCardScale = 0.5
        for idx, card in enumerate(self.avaliableCard):
            if idx//4 == self.avaliableCardIndex//4:
                card.renderPosition(screen, (SCREEN_WIDTH*0.75 + self.avaliableCardSpacing, SCREEN_HEIGHT*0.2 + self.avaliableCardSpacing + SCREEN_HEIGHT*0.2*(idx%4)), avaliableCardScale)
                screen.blit(pygame.font.Font(None, 48).render(card.name, True, (0,0,0)), (SCREEN_WIDTH*0.75 + self.avaliableCardSpacing, SCREEN_HEIGHT*0.2 + self.avaliableCardSpacing + SCREEN_HEIGHT*0.2*(idx%4)))
        
        # render selected card detail
        if self.selectDeck and len(self.deck.card_deck) !=0:
            card = self.deck.card_deck[self.deckIndex]
        elif not self.selectDeck and len(self.avaliableCard)!=0:
            card = self.avaliableCard[self.avaliableCardIndex]
        card.renderPosition(screen, (self.selectedCardSpacing , self.selectedCardSpacing), 1)
        screen.blit(pygame.font.Font(None, 48).render(card.name, True, (0,0,0)),(self.selectedCardSpacing , self.selectedCardSpacing))
        screen.blit(pygame.font.Font(None, 24).render("damage : " + str(card.dmg), True, (0,0,0)),(self.selectedCardSpacing , self.selectedCardSpacing + CARD_HEIGHT + 20))
        screen.blit(pygame.font.Font(None, 24).render("range : " + str(card.range), True, (0,0,0)),(self.selectedCardSpacing , self.selectedCardSpacing + CARD_HEIGHT + 70))
        screen.blit(pygame.font.Font(None, 24).render("defend : " + str(card.defend), True, (0,0,0)),(self.selectedCardSpacing , self.selectedCardSpacing + CARD_HEIGHT + 120))
        screen.blit(pygame.font.Font(None, 24).render("speed : " + str(card.speed), True, (0,0,0)),(self.selectedCardSpacing , self.selectedCardSpacing + CARD_HEIGHT + 170))
        screen.blit(pygame.font.Font(None, 24).render("description : " + card.description, True, (0,0,0)),(self.selectedCardSpacing , self.selectedCardSpacing + CARD_HEIGHT + 220))
    
        
        
        # render highlight for selection        
        if self.selectDeck:
            pygame.draw.rect(screen, (255,255,0), (SCREEN_WIDTH * 0.25 + self.deckSpacing + (CARD_WIDTH*deckScale + self.deckSpacing)*(self.deckIndex%self.cardPerRow) ,SCREEN_HEIGHT*0.2 + self.deckSpacing+ (CARD_HEIGHT*deckScale + self.deckSpacing)*(self.deckIndex//self.cardPerRow), CARD_WIDTH * deckScale, CARD_HEIGHT * deckScale), 3)
        else:
            pygame.draw.rect(screen, (255,255,0), (SCREEN_WIDTH*0.75 + self.avaliableCardSpacing, SCREEN_HEIGHT*0.2 + self.avaliableCardSpacing + SCREEN_HEIGHT*0.2*(self.avaliableCardIndex%4), CARD_WIDTH* avaliableCardScale, CARD_HEIGHT* avaliableCardScale),3)


        # render instruction
        screen.blit(pygame.font.Font(None, 24).render("The middle section is the deck and the right section is the avaliable card to put in the deck", True, (0,0,0)),(SCREEN_WIDTH*0.25 +  self.selectedCardSpacing , self.selectedCardSpacing))
        screen.blit(pygame.font.Font(None, 24).render("Use 'ARROW' key to nevigate and select card you want to choose    'SPCAE' to choose card to deck or remove it", True, (0,0,0)),(SCREEN_WIDTH*0.25 +  self.selectedCardSpacing , self.selectedCardSpacing + 50))
        screen.blit(pygame.font.Font(None, 24).render("Press 'ENTER' to go back to preparation state", True, (0,0,0)),(SCREEN_WIDTH*0.25 +  self.selectedCardSpacing , self.selectedCardSpacing + 100))

            
