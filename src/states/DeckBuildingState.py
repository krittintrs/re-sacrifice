from src.cardSystem.Deck import Deck
from src.states.BaseState import BaseState
from src.dependency import *
from src.constants import *
import pygame
import sys

class DeckBuildingState(BaseState):

    def __init__(self):
        super(DeckBuildingState, self).__init__()
        self.availableCard = []
        self.inventory = []
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

        self.leftPanel = pygame.Rect((0,0, self.leftBorder, SCREEN_HEIGHT))
        self.topPanel = pygame.Rect((self.leftBorder,0, self.rightBorder, self.topBorder))
        self.middlePanel = pygame.Rect((self.leftBorder, self.topBorder, SCREEN_WIDTH*0.5, SCREEN_HEIGHT*0.8))
        self.rightPanel = pygame.Rect((self.rightBorder, self.topBorder, self.leftBorder, SCREEN_HEIGHT*0.8))

        self.buttons = []
        for idx, effect in enumerate(EffectType):
            button = Button(self.rightBorder -200 +83*(idx%6), self.topBorder - 120 + 28*(idx//6), 80, 25,(150,150,150), (100,200,100), (100,100,50), effect.value, 20)
            self.buttons.append(button)

        self.deckScale = (self.rightBorder - self.leftBorder)/((CARD_WIDTH + self.deckSpacing*3)*self.cardPerRow)
        self.availableCardScale = 0.5

        self.scroll_speed = 1
        # mock inventory card
        for card in card_dict.values():
            self.inventory.append(card)
        

    def Enter(self, params):
        self.player = params['player']
        self.player.deck = Deck()

        self.availableCard = self.inventory

    def Exit(self):
        pass
    
    def filter(self, types, classes, effects):
        result = []
        for card in self.inventory:
            card_effect = set()
            for effect in (card.beforeEffect + card.mainEffect + card.afterEffect):
                card_effect.add(effect.type)
            if effects.issubset(card_effect):
                result.append(card)
            elif card.type in types:
                result.append(card)
            elif card.class_ in classes:
                result.append(card)
            # elif card.be
        return result


    def update(self, dt, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            mouse_pos = pygame.mouse.get_pos()
            # high light card that mouse hover on
            # deck
            if self.middlePanel.collidepoint(mouse_pos):
                for idx in range(0,len(self.player.deck.card_deck)):
                    rect = pygame.Rect((self.leftBorder + self.deckSpacing + (CARD_WIDTH*self.deckScale + self.deckSpacing)*(idx%self.cardPerRow), self.topBorder + self.deckSpacing + (CARD_HEIGHT*self.deckScale + self.deckSpacing)*(idx//self.cardPerRow),int(CARD_WIDTH * self.deckScale), int(CARD_HEIGHT * self.deckScale)))
                    if rect.collidepoint(mouse_pos):
                        self.isMouseOn = True
                        self.selectDeck = True
                        self.deckIndex = idx
                        break
                    else:
                        self.isMouseOn = False

            # available card
            elif self.rightPanel.collidepoint(mouse_pos):
                for i in range(0, min(4,len(self.availableCard)-self.availableCardWindow)):
                    rect = pygame.Rect((self.rightBorder + self.availableCardSpacing, self.topBorder + self.availableCardSpacing + self.topBorder*(i),int(CARD_WIDTH * self.availableCardScale), int(CARD_HEIGHT * self.availableCardScale)))
                    if rect.collidepoint(mouse_pos):
                        self.isMouseOn = True
                        self.selectDeck = False
                        self.availableCardIndex = self.availableCardWindow + i
                        break
                    else:
                        self.isMouseOn = False
            else:
                self.isMouseOn = False
            


            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left-click
                    effects = set()
                    for button in self.buttons:
                        button.is_clicked(event)
                        if button.clicked:
                            effects.add(button.text)
                    self.availableCard = self.filter([],[],effects).copy()
                    print(len(self.availableCard))
                    if self.isMouseOn and self.selectDeck:
                        if len(self.player.deck.card_deck)!=0:
                            card = self.player.deck.card_deck[self.deckIndex]
                            self.availableCard.append(card)
                            self.inventory.append(card)
                            self.player.deck.removeCard(card)
                            if self.deckIndex >= len(self.player.deck.card_deck) - 1 and self.deckIndex != 0:
                                self.deckIndex -= 1
                            print('player deck size AFTER RM: ', len(self.player.deck.card_deck))
                    elif self.isMouseOn and not self.selectDeck:
                        if len(self.availableCard)!=0 and not self.player.deck.isCardLimitReach():
                            card = self.availableCard.pop(self.availableCardIndex)
                            self.inventory.remove(card)
                            self.player.deck.addCard(card)
                            if self.availableCardIndex >= len(self.availableCard)- 1 and self.availableCardIndex != 0:
                                self.availableCardIndex -= 1
                            print('player deck size AFTER ADD: ', len(self.player.deck.card_deck))



            if event.type == pygame.MOUSEWHEEL and self.rightPanel.collidepoint(mouse_pos):
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
                        'player': self.player,
                        'enemy': None
                    })

            

    def render(self, screen):
        screen.fill((255,255,255))

        # layout
        
        pygame.draw.rect(screen, (255,255,0), self.leftPanel, 5)
        pygame.draw.rect(screen, (255,0,0), self.topPanel, 5)
        pygame.draw.rect(screen, (0,255,0), self.middlePanel , 5)
        pygame.draw.rect(screen, (0,0,255), self.rightPanel, 5)

        # render deck
        self.deckScale = (SCREEN_WIDTH*0.5)/((CARD_WIDTH + self.deckSpacing*3)*self.cardPerRow)
        for idx, card in enumerate(self.player.deck.card_deck):
            scaled_image = pygame.transform.scale(card.image, (int(CARD_WIDTH * self.deckScale), int(CARD_HEIGHT * self.deckScale)))
            screen.blit(scaled_image, (self.leftBorder + self.deckSpacing + (CARD_WIDTH*self.deckScale + self.deckSpacing)*(idx%self.cardPerRow), self.topBorder + self.deckSpacing + (CARD_HEIGHT*self.deckScale + self.deckSpacing)*(idx//self.cardPerRow)))
        
        # render available cards
        self.availableCardScale = 0.5
        for idx, card in enumerate(self.availableCard):
            if idx in range(self.availableCardWindow, self.availableCardWindow + 4):
                scaled_image = pygame.transform.scale(card.image, (int(CARD_WIDTH * self.availableCardScale), int(CARD_HEIGHT * self.availableCardScale)))
                screen.blit(scaled_image, (self.rightBorder + self.availableCardSpacing, self.topBorder + self.availableCardSpacing + self.topBorder*(idx-self.availableCardWindow)))
        # render selected card detail
        if self.selectDeck and len(self.player.deck.card_deck) !=0:
            card = self.player.deck.card_deck[self.deckIndex]
            screen.blit(card.image, (self.selectedCardSpacing, self.selectedCardSpacing))
            screen.blit(pygame.font.Font(None, 36).render(card.name, True, (0,0,0)),(self.selectedCardSpacing , self.selectedCardSpacing + CARD_HEIGHT + 10))
            screen.blit(pygame.font.Font(None, 24).render("damage : " + str(card.attack), True, (0,0,0)),(self.selectedCardSpacing , self.selectedCardSpacing + CARD_HEIGHT + 50))
            screen.blit(pygame.font.Font(None, 24).render("range : " + str(card.range_end), True, (0,0,0)),(self.selectedCardSpacing , self.selectedCardSpacing + CARD_HEIGHT + 80))
            screen.blit(pygame.font.Font(None, 24).render("defend : " + str(card.defense), True, (0,0,0)),(self.selectedCardSpacing , self.selectedCardSpacing + CARD_HEIGHT + 110))
            screen.blit(pygame.font.Font(None, 24).render("speed : " + str(card.speed), True, (0,0,0)),(self.selectedCardSpacing , self.selectedCardSpacing + CARD_HEIGHT + 140))
            screen.blit(pygame.font.Font(None, 24).render("description : " + card.description, True, (0,0,0)),(self.selectedCardSpacing , self.selectedCardSpacing + CARD_HEIGHT + 170))
    
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
        screen.blit(pygame.font.Font(None, 24).render(f"Deck {len(self.player.deck.card_deck)}/30", True, (0,0,0)),(self.rightBorder - 100 , self.topBorder -20))
        screen.blit(pygame.font.Font(None, 24).render(f"Available Cards {len(self.availableCard)}", True, (0,0,0)),(SCREEN_WIDTH - 160 , self.topBorder -20))


        # render scroll wheel
        if len(self.availableCard) != 0:
            scroll_wheel_y = self.topBorder + ((SCREEN_HEIGHT*0.8-60)/len(self.availableCard) * self.availableCardWindow)
            pygame.draw.rect(screen, (100,100,100), (SCREEN_WIDTH * 0.98, scroll_wheel_y, SCREEN_WIDTH * 0.02, 60))

        # render filter button
        for button in self.buttons:
            button.draw(screen)




class Button:
    def __init__(self, x, y, width, height, color, clicked_color, hover_color, text='', font_size=30):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.clicked_color = clicked_color
        self.hover_color = hover_color
        self.text = text
        self.clicked = False
        self.font = pygame.font.Font(None, font_size)
        self.text_surface = self.font.render(self.text, True, (0,0,0))
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)
        
    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, self.hover_color, self.rect)
        elif self.clicked:
            pygame.draw.rect(screen, self.clicked_color, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)
        screen.blit(self.text_surface, self.text_rect)

    def is_clicked(self, event):
        if self.rect.collidepoint(event.pos):
            self.clicked = not self.clicked
            return True
        return False
