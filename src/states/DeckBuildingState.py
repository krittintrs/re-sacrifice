from src.states.BaseState import BaseState
from src.dependency import *
from src.constants import *
import pygame
import sys

class DeckBuildingState(BaseState):

    def __init__(self):
        super(DeckBuildingState, self).__init__()
        self.availableCard = []
        self.selectDeck = True
        self.deckIndex = 0
        self.availableCardIndex = 0
        self.cardPerRow = 8
        self.availableCardSpacing = 10
        self.deckSpacing = 5
        self.selectedCardSpacing = 20
        self.availableCardWindow = 0
        self.isMouseOn = False
        
        self.leftBorder = SCREEN_WIDTH * 0.25
        self.topBorder = SCREEN_HEIGHT * 0.2
        self.rightBorder = SCREEN_WIDTH * 0.75

        self.left_panel = pygame.Rect((0,0, self.leftBorder, SCREEN_HEIGHT))
        self.top_panel = pygame.Rect((self.leftBorder,0, self.rightBorder, self.topBorder))
        self.middle_panel = pygame.Rect((self.leftBorder, self.topBorder, SCREEN_WIDTH*0.5, SCREEN_HEIGHT*0.8))
        self.right_panel = pygame.Rect((self.rightBorder, self.topBorder, self.leftBorder, SCREEN_HEIGHT*0.8))

        self.deckScale = (self.rightBorder - self.leftBorder)/((CARD_WIDTH + self.deckSpacing*3)*self.cardPerRow)
        self.availableCardScale = 0.5

        self.scroll_speed = 1
        # mock available card
        for card in card_dict.values():
            self.availableCard.append(card)
        

    def Enter(self, params):
        self.deck = params["deck"]

    def Exit(self):
        pass
    

    def update(self, dt, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            mouse_pos = pygame.mouse.get_pos()
            # high light card that mouse hover on
            # deck
            if self.middle_panel.collidepoint(mouse_pos):
                for idx in range(0,len(self.deck.card_deck)):
                    rect = pygame.Rect((self.leftBorder + self.deckSpacing + (CARD_WIDTH*self.deckScale + self.deckSpacing)*(idx%self.cardPerRow), self.topBorder + self.deckSpacing + (CARD_HEIGHT*self.deckScale + self.deckSpacing)*(idx//self.cardPerRow),int(CARD_WIDTH * self.deckScale), int(CARD_HEIGHT * self.deckScale)))
                    if rect.collidepoint(mouse_pos):
                        self.isMouseOn = True
                        self.selectDeck = True
                        self.deckIndex = idx
                        break
                    else:
                        self.isMouseOn = False

            # available card
            if self.right_panel.collidepoint(mouse_pos):
                for i in range(0, min(4,len(self.availableCard)-self.availableCardWindow)):
                    rect = pygame.Rect((self.rightBorder + self.availableCardSpacing, self.topBorder + self.availableCardSpacing + self.topBorder*(i),int(CARD_WIDTH * self.availableCardScale), int(CARD_HEIGHT * self.availableCardScale)))
                    if rect.collidepoint(mouse_pos):
                        self.isMouseOn = True
                        self.selectDeck = False
                        self.availableCardIndex = self.availableCardWindow + i
                        break
                    else:
                        self.isMouseOn = False


            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left-click
                    if self.isMouseOn and self.selectDeck:
                        if len(self.deck.card_deck)!=0:
                            if self.deckIndex == len(self.deck.card_deck) - 1 and self.deckIndex != 0:
                                self.deckIndex -= 1
                            card = self.deck.card_deck[self.deckIndex]
                            self.availableCard.append(card)
                            self.deck.removeCard(card)
                    elif self.isMouseOn and not self.selectDeck:
                        if len(self.availableCard)!=0 and not self.deck.isCardLimitReach():
                            if self.availableCardIndex == len(self.availableCard)- 1 and self.availableCardIndex != 0:
                                self.availableCardIndex -= 1
                            card = self.availableCard.pop(self.availableCardIndex)
                            self.deck.addCard(card)


            if event.type == pygame.MOUSEWHEEL and self.right_panel.collidepoint(mouse_pos):
                self.availableCardWindow -= event.y * self.scroll_speed
                if self.availableCardWindow < 0:
                    self.availableCardWindow = 0
                elif self.availableCardWindow > len(self.availableCard) - 1:
                    self.availableCardWindow = len(self.availableCard) - 1

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_RETURN:
                    g_state_manager.Change(BattleState.PREPARATION_PHASE, {
                        'player': None,
                        'enemy': None
                    })

    def render(self, screen):
        screen.fill((255,255,255))

        # layout
        
        pygame.draw.rect(screen, (255,255,0), self.left_panel, 5)
        pygame.draw.rect(screen, (255,0,0), self.top_panel, 5)
        pygame.draw.rect(screen, (0,255,0), self.middle_panel , 5)
        pygame.draw.rect(screen, (0,0,255), self.right_panel, 5)

        # render deck
        self.deckScale = (SCREEN_WIDTH*0.5)/((CARD_WIDTH + self.deckSpacing*3)*self.cardPerRow)
        for idx, card in enumerate(self.deck.card_deck):
            scaled_image = pygame.transform.scale(card.image, (int(CARD_WIDTH * self.deckScale), int(CARD_HEIGHT * self.deckScale)))
            screen.blit(scaled_image, (self.leftBorder + self.deckSpacing + (CARD_WIDTH*self.deckScale + self.deckSpacing)*(idx%self.cardPerRow), self.topBorder + self.deckSpacing + (CARD_HEIGHT*self.deckScale + self.deckSpacing)*(idx//self.cardPerRow)))
        
        # render available cards
        self.availableCardScale = 0.5
        for idx, card in enumerate(self.availableCard):
            if idx in range(self.availableCardWindow, self.availableCardWindow + 4):
                scaled_image = pygame.transform.scale(card.image, (int(CARD_WIDTH * self.availableCardScale), int(CARD_HEIGHT * self.availableCardScale)))
                screen.blit(scaled_image, (self.rightBorder + self.availableCardSpacing, self.topBorder + self.availableCardSpacing + self.topBorder*(idx-self.availableCardWindow)))
        # render selected card detail
        if self.selectDeck and len(self.deck.card_deck) !=0:
            card = self.deck.card_deck[self.deckIndex]
        elif not self.selectDeck and len(self.availableCard)!=0:
            card = self.availableCard[self.availableCardIndex]
        screen.blit(card.image, (self.selectedCardSpacing, self.selectedCardSpacing))
        screen.blit(pygame.font.Font(None, 36).render(card.name, True, (0,0,0)),(self.selectedCardSpacing , self.selectedCardSpacing + CARD_HEIGHT + 10))
        screen.blit(pygame.font.Font(None, 24).render("damage : " + str(card.attack), True, (0,0,0)),(self.selectedCardSpacing , self.selectedCardSpacing + CARD_HEIGHT + 50))
        screen.blit(pygame.font.Font(None, 24).render("range : " + str(card.range_end), True, (0,0,0)),(self.selectedCardSpacing , self.selectedCardSpacing + CARD_HEIGHT + 80))
        screen.blit(pygame.font.Font(None, 24).render("defend : " + str(card.defense), True, (0,0,0)),(self.selectedCardSpacing , self.selectedCardSpacing + CARD_HEIGHT + 110))
        screen.blit(pygame.font.Font(None, 24).render("speed : " + str(card.speed), True, (0,0,0)),(self.selectedCardSpacing , self.selectedCardSpacing + CARD_HEIGHT + 140))
        screen.blit(pygame.font.Font(None, 24).render("description : " + card.description, True, (0,0,0)),(self.selectedCardSpacing , self.selectedCardSpacing + CARD_HEIGHT + 170))
    
        
        
        # render highlight for selection        
        if self.selectDeck:
            pygame.draw.rect(screen, (255,255,0), (self.leftBorder + self.deckSpacing + (CARD_WIDTH*self.deckScale + self.deckSpacing)*(self.deckIndex%self.cardPerRow) ,self.topBorder + self.deckSpacing+ (CARD_HEIGHT*self.deckScale + self.deckSpacing)*(self.deckIndex//self.cardPerRow), CARD_WIDTH*self.deckScale, CARD_HEIGHT*self.deckScale), 3)
        else:
            pygame.draw.rect(screen, (255,255,0), (self.rightBorder + self.availableCardSpacing, self.topBorder + self.availableCardSpacing + self.topBorder*((self.availableCardIndex- self.availableCardWindow%4)%4) , CARD_WIDTH* self.availableCardScale, CARD_HEIGHT* self.availableCardScale),3)


        # render deck and available card information
        screen.blit(pygame.font.Font(None, 24).render(f"Deck {len(self.deck.card_deck)}/30", True, (0,0,0)),(self.rightBorder - 100 , self.topBorder -20))
        screen.blit(pygame.font.Font(None, 24).render(f"Available Cards {len(self.availableCard)}", True, (0,0,0)),(SCREEN_WIDTH - 160 , self.topBorder -20))


        # render scroll wheel
        scroll_wheel_y = self.topBorder + ((SCREEN_HEIGHT*0.8-60)/len(self.availableCard) * self.availableCardWindow)
        pygame.draw.rect(screen, (100,100,100), (SCREEN_WIDTH * 0.98, scroll_wheel_y, SCREEN_WIDTH * 0.02, 60))
            
