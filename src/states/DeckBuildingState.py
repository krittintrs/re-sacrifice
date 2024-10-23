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
        self.cardClass = CardClass #[CardClass.COMMON, CardClass.WARRIOR, CardClass.RANGER, CardClass.MAGE]
        self.cardEffect = [EffectType.ATTACK, EffectType.MOVE, EffectType.SELF_BUFF, EffectType.RANGE_BUFF, EffectType.PULL, EffectType.PUSH, EffectType.DEBUFF, EffectType.BUFF, EffectType.CLEANSE, EffectType.HEAL, EffectType.DISCARD]
        
        self.leftBorder = SCREEN_WIDTH * 0.25
        self.topBorder = SCREEN_HEIGHT * 0.2
        self.rightBorder = SCREEN_WIDTH * 0.75

        self.leftPanel = pygame.Rect((0,0, self.leftBorder, SCREEN_HEIGHT))
        self.topPanel = pygame.Rect((self.leftBorder,0, self.rightBorder, self.topBorder))
        self.middlePanel = pygame.Rect((self.leftBorder, self.topBorder, SCREEN_WIDTH*0.5, SCREEN_HEIGHT*0.8))
        self.rightPanel = pygame.Rect((self.rightBorder, self.topBorder, self.leftBorder, SCREEN_HEIGHT*0.8))

        self.effectButton = []
        for idx, effect in enumerate(self.cardEffect):
            button = Button(self.rightBorder  +73*(idx%4), self.topBorder - 105 + 28*(idx//4), 70, 25,(150,150,150), (100,200,100), (100,100,50), effect.value, 15)
            self.effectButton.append(button)

        self.classButton = []
        for idx, class_ in enumerate(self.cardClass):
            button = Button(self.leftBorder+10 +83*idx, self.topBorder - 115, 80, 25,(150,150,150), (100,200,100), (100,100,50), class_.value, 20)
            self.classButton.append(button)

        self.typeButton = []
        for idx, type in enumerate(CardType):
            button = Button(self.leftBorder+10 +83*idx, self.topBorder - 60, 80, 25,(150,150,150), (100,200,100), (100,100,50), type.value, 20)
            self.typeButton.append(button)

        self.sortButton = Button(self.leftBorder + 100, self.topBorder - 30 , 80, 25,(150,150,150), (100,200,100), (100,100,50), "sort", 20)

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
    
    def filter(self, types, classes, effects): # each argument represent condition ex. types = ["Move"]
        result = []
        # flag to check condition
        type_flag = False
        class_flag = False
        effect_flag = False

        for card in self.inventory:
            # get a set of card effect type
            card_effect = set()
            for effect in (card.beforeEffect + card.mainEffect + card.afterEffect):
                card_effect.add(effect.type)

            # check condition
            effect_flag = effects.issubset(card_effect)
            type_flag = card.type in types
            class_flag = card.class_ in classes

            if effect_flag and type_flag and class_flag:
                result.append(card)
        return result

    # sort card based on ID
    def sort_card(self,cards):
        cards.sort(key=lambda card: int(card.id[1:]))


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
                    # if mouse click filter
                    effects = set()
                    types = []
                    classes = []
                    for button in self.effectButton:
                        button.clicked(event)
                        if button.isClick:
                            effects.add(button.text)
                            self.availableCardWindow = 0
                    for button in self.classButton:
                        button.clicked(event)
                        if button.isClick:
                            classes.append(button.text)
                            self.availableCardWindow = 0
                    for button in self.typeButton:
                        button.clicked(event)
                        if button.isClick:
                            types.append(button.text)
                            self.availableCardWindow = 0
                    # if no type filter is selected > select all
                    if len(types)==0:
                        for type in CardType:
                            types.append(type.value)

                    # if no class filter is selected > select all
                    if len(classes)==0:
                        for class_ in self.cardClass:
                            classes.append(class_.value)
    
                    # filter available card
                    self.availableCard = self.filter(types,classes,effects).copy()

                    


                    #click card on deck
                    if self.isMouseOn and self.selectDeck:
                        if len(self.player.deck.card_deck)!=0:
                            card = self.player.deck.card_deck[self.deckIndex]
                            self.availableCard.append(card)
                            self.inventory.append(card)
                            self.player.deck.removeCard(card)
                            if self.deckIndex >= len(self.player.deck.card_deck) - 1 and self.deckIndex != 0:
                                self.deckIndex -= 1
                            print('player deck size AFTER RM: ', len(self.player.deck.card_deck))
                    # click card on available list
                    elif self.isMouseOn and not self.selectDeck:
                        if len(self.availableCard)!=0 and not self.player.deck.isCardLimitReach():
                            card = self.availableCard.pop(self.availableCardIndex)
                            self.inventory.remove(card)
                            self.player.deck.addCard(card)
                            if self.availableCardIndex >= len(self.availableCard)- 1 and self.availableCardIndex != 0:
                                self.availableCardIndex = (self.availableCardIndex -1)%4 
                                self.availableCardWindow = max(0,self.availableCardWindow-1)
                            print('player deck size AFTER ADD: ', len(self.player.deck.card_deck))

                    # click sort button
                    if self.sortButton.clicked(event):
                        self.sortButton.isClick = False
                        self.sort_card(self.availableCard)
                        self.sort_card(self.player.deck.card_deck)
                        self.sort_card(self.inventory)
                        self.availableCardWindow = 0


                    



            if event.type == pygame.MOUSEWHEEL and self.rightPanel.collidepoint(mouse_pos):
                self.availableCardWindow -= event.y * self.scroll_speed
                if self.availableCardWindow < 0 or len(self.availableCard) <= 4:
                    self.availableCardWindow = 0
                elif self.availableCardWindow > len(self.availableCard) - 4:
                    self.availableCardWindow = len(self.availableCard) - 4

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
                screen.blit(pygame.font.Font(None, 20).render( card.name, True, (0,0,0)),(self.rightBorder + self.availableCardSpacing + 120, self.topBorder +10+ self.availableCardSpacing + self.topBorder*(idx-self.availableCardWindow)))
                screen.blit(pygame.font.Font(None, 17).render( card.type, True, (0,0,0)),(self.rightBorder + self.availableCardSpacing + 120, self.topBorder +40+ self.availableCardSpacing + self.topBorder*(idx-self.availableCardWindow)))
                screen.blit(pygame.font.Font(None, 15).render( "ATK: "+str(card.attack)+" DEF: "+str(card.defense)+" Range: "+str(card.range_start)+"-"+str(card.range_end)+" SPD: "+str(card.speed), True, (0,0,0)),(self.rightBorder + self.availableCardSpacing + 120, self.topBorder +70+ self.availableCardSpacing + self.topBorder*(idx-self.availableCardWindow)))
        # render selected card detail
        if self.selectDeck and len(self.player.deck.card_deck) !=0 and self.deckIndex < len(self.player.deck.card_deck):
            card = self.player.deck.card_deck[self.deckIndex]
            screen.blit(card.image, (self.selectedCardSpacing, self.selectedCardSpacing))
            screen.blit(pygame.font.Font(None, 36).render(card.name, True, (0,0,0)),(self.selectedCardSpacing , self.selectedCardSpacing + CARD_HEIGHT + 10))
            screen.blit(pygame.font.Font(None, 24).render("damage : " + str(card.attack), True, (0,0,0)),(self.selectedCardSpacing , self.selectedCardSpacing + CARD_HEIGHT + 50))
            screen.blit(pygame.font.Font(None, 24).render("range : " + str(card.range_end), True, (0,0,0)),(self.selectedCardSpacing , self.selectedCardSpacing + CARD_HEIGHT + 80))
            screen.blit(pygame.font.Font(None, 24).render("defend : " + str(card.defense), True, (0,0,0)),(self.selectedCardSpacing , self.selectedCardSpacing + CARD_HEIGHT + 110))
            screen.blit(pygame.font.Font(None, 24).render("speed : " + str(card.speed), True, (0,0,0)),(self.selectedCardSpacing , self.selectedCardSpacing + CARD_HEIGHT + 140))
            screen.blit(pygame.font.Font(None, 24).render("description : " + card.description, True, (0,0,0)),(self.selectedCardSpacing , self.selectedCardSpacing + CARD_HEIGHT + 170))
    
        elif not self.selectDeck and len(self.availableCard)!=0 and self.availableCardIndex < len(self.availableCard):
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
        for button in self.effectButton:
            button.draw(screen)

        for button in self.typeButton:
            button.draw(screen)

        for button in self.classButton:
            button.draw(screen)
        
        # render filter description
        screen.blit(pygame.font.Font(None, 30).render("Card Class", True, (0,0,0)),(self.leftBorder +15, 10))
        screen.blit(pygame.font.Font(None, 30).render("Card Type", True, (0,0,0)),(self.leftBorder +15, self.topBorder -80))
        screen.blit(pygame.font.Font(None, 30).render("Effect Type", True, (0,0,0)),(self.rightBorder +80, 10))

        # render sort button
        self.sortButton.draw(screen)







class Button:
    def __init__(self, x, y, width, height, color, clicked_color, hover_color, text='', font_size=30):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.clicked_color = clicked_color
        self.hover_color = hover_color
        self.text = text
        self.isClick = False
        self.font = pygame.font.Font(None, font_size)
        self.text_surface = self.font.render(self.text, True, (0,0,0))
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)
        
    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, self.hover_color, self.rect)
        elif self.isClick:
            pygame.draw.rect(screen, self.clicked_color, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)
        screen.blit(self.text_surface, self.text_rect)

    def clicked(self, event):
        if self.rect.collidepoint(event.pos):
            self.isClick = not self.isClick
            return True
        else:
            return False