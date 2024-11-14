from src.battleSystem.Card import Card
from src.battleSystem.Deck import Deck
from src.states.BaseState import BaseState
from src.dependency import *
from src.constants import *
from src.Render import *
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
        self.selectedCardSpacing = 25
        self.availableCardWindow = 0
        self.isMouseOn = False
        self.cardClass = list(CardClass)
        self.cardEffect = [EffectType.ATTACK, EffectType.MOVE, EffectType.SELF_BUFF, EffectType.OPPO_BUFF, EffectType.PULL, EffectType.PUSH, EffectType.CLEANSE]
        
        self.leftBorder = SCREEN_WIDTH * 0.25
        self.topBorder = SCREEN_HEIGHT * 0.2
        self.rightBorder = SCREEN_WIDTH * 0.75

        self.leftPanelX = DECK_OFFSET
        self.leftPanelY = DECK_OFFSET
        self.leftPanelWidth = self.leftBorder - DECK_OFFSET*2
        self.leftPanelHeight = SCREEN_HEIGHT - DECK_OFFSET*2

        self.topPanelX = self.leftBorder + DECK_OFFSET
        self.topPanelY = DECK_OFFSET
        self.topPanelWidth = self.rightBorder - DECK_OFFSET*2
        self.topPanelHeight = self.topBorder - DECK_OFFSET*2

        self.middlePanelX = self.topPanelX
        self.middlePanelY = self.topBorder + DECK_OFFSET
        self.middlePanelWidth = SCREEN_WIDTH*0.5 - DECK_OFFSET*2
        self.middlePanelHeight = SCREEN_HEIGHT*0.8 - DECK_OFFSET*2

        self.rightPanelX = self.rightBorder + DECK_OFFSET
        self.rightPanelY = self.middlePanelY
        self.rightPanelWidth = self.leftBorder - DECK_OFFSET*2
        self.rightPanelHeight = self.middlePanelHeight

        self.leftPanel = pygame.Rect((
            self.leftPanelX, self.leftPanelY, self.leftPanelWidth, self.leftPanelHeight
        ))
        self.topPanel = pygame.Rect((
            self.topPanelX, self.topPanelY, self.topPanelWidth, self.topPanelHeight
        ))
        print(self.topPanelX, self.topPanelY, self.topPanelWidth, self.topPanelHeight)
        self.middlePanel = pygame.Rect((
            self.middlePanelX, self.middlePanelY, self.middlePanelWidth, self.middlePanelHeight
        ))
        self.rightPanel = pygame.Rect((
            self.rightPanelX, self.rightPanelY, self.rightPanelWidth, self.rightPanelHeight
        ))

        self.effectButton = []
        for idx, effect in enumerate(self.cardEffect):
            button = Button(self.rightPanelX - 60 + (BUTTON_WIDTH+3)*(idx%4), self.topPanelY + BUTTON_UPPER_OFFSET + 28*(idx//4), BUTTON_WIDTH, BUTTON_HEIGHT, effect.value)
            self.effectButton.append(button)

        self.classButton = []
        for idx, class_ in enumerate(self.cardClass):
            button = Button(self.topPanelX+10 + (BUTTON_WIDTH+3)*idx, self.topPanelY + BUTTON_UPPER_OFFSET, BUTTON_WIDTH, BUTTON_HEIGHT, class_.value)
            self.classButton.append(button)

        self.typeButton = []
        for idx, type in enumerate(CardType):
            button = Button(self.topPanelX+10 + (BUTTON_WIDTH+3)*idx, self.topPanelY + BUTTON_LOWER_OFFSET, BUTTON_WIDTH, BUTTON_HEIGHT, type.value)
            self.typeButton.append(button)

        self.sortButton = Button(self.topPanelX+10, self.topPanelY + BUTTON_LOWER_OFFSET + BUTTON_HEIGHT + 5, BUTTON_WIDTH, BUTTON_HEIGHT, "sort")

        self.availableCardScale = 0.5

        self.scroll_speed = 1
        

    def Enter(self, params):
        self.params = params
        battle_param = self.params['battleSystem']
        self.edit_player_deck = battle_param['edit_player_deck']
        if self.edit_player_deck:
            self.player = battle_param['player']
            self.enemy = battle_param['enemy']
        else:
            self.player = battle_param['enemy']
            self.enemy = battle_param['player']
        # if the inventory is empty give the default inventory to player
        if len(self.player.deck.inventory) == 0:
            print("Player inventory is empty")
            self.player.deck.readInventoryConf(DECK_DEFS["default_inventory"])
            
        self.inventory = self.player.deck.inventory
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
                card_effect.add(effect.type.value)

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
                    rect = pygame.Rect((self.middlePanelX + self.deckSpacing + (CARD_WIDTH*self.deckScale + self.deckSpacing)*(idx%self.cardPerRow), self.topBorder + self.deckSpacing + (CARD_HEIGHT*self.deckScale + self.deckSpacing)*(idx//self.cardPerRow),int(CARD_WIDTH * self.deckScale), int(CARD_HEIGHT * self.deckScale)))
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
                    card_x = self.rightPanelX + self.availableCardSpacing
                    card_y = self.rightPanelY + self.availableCardSpacing + (self.rightPanelY - self.availableCardSpacing*2 -10)*(i)
                    rect = pygame.Rect((card_x, card_y ,int(CARD_WIDTH * self.availableCardScale), int(CARD_HEIGHT * self.availableCardScale)))
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
                elif event.key == pygame.K_d:
                    self.deckIndex = 0
                    self.player.deck.read_conf(DECK_DEFS["default"])
                elif event.key == pygame.K_w:
                    self.deckIndex = 0
                    self.player.deck.read_conf(DECK_DEFS["warrior"])
                elif event.key == pygame.K_r:
                    self.deckIndex = 0
                    self.player.deck.read_conf(DECK_DEFS["ranger"])
                elif event.key == pygame.K_m:
                    self.deckIndex = 0
                    self.player.deck.read_conf(DECK_DEFS["mage"])

                elif event.key == pygame.K_RETURN:
                    if self.player.deck.isCardMinimumReach():
                        if self.player.deck.isCardDuplicateWithinLimit():
                            destination_state = self.params['battleSystem']['from_state']
                            if self.edit_player_deck:
                                self.params['battleSystem'] = {
                                    'player': self.player,
                                    'enemy': self.enemy
                                }
                                g_state_manager.Change(destination_state, self.params)
                            else:
                                self.params['battleSystem'] = {
                                    'player': self.enemy,
                                    'enemy': self.player
                                }
                                g_state_manager.Change(destination_state, self.params)
                        else:
                            print("Player deck must not have more than 3 duplicate of cards")
                    else:
                        print("Player deck must have at least 20 cards")

    def render(self, screen):
        RenderBackground(screen, BackgroundState.DECK_BUILDING)
        
        # pygame.draw.rect(screen, (255,255,0), self.leftPanel, 1)
        # pygame.draw.rect(screen, (255,0,0), self.topPanel, 1)
        # pygame.draw.rect(screen, (0,255,0), self.middlePanel , 1)
        # pygame.draw.rect(screen, (0,0,255), self.rightPanel, 1)

        # render deck
        self.deckScale = self.middlePanelWidth/((CARD_WIDTH + self.deckSpacing*3)*self.cardPerRow)
        for idx, card in enumerate(self.player.deck.card_deck):
            scaled_image = pygame.transform.scale(card.image, (int(CARD_WIDTH * self.deckScale), int(CARD_HEIGHT * self.deckScale)))
            screen.blit(scaled_image, (self.middlePanelX + self.deckSpacing + (CARD_WIDTH*self.deckScale + self.deckSpacing)*(idx%self.cardPerRow), self.middlePanelY + self.deckSpacing + (CARD_HEIGHT*self.deckScale + self.deckSpacing)*(idx//self.cardPerRow)))
        
        # render available cards
        self.availableCardScale = 0.5
        for idx, card in enumerate(self.availableCard):
            if idx in range(self.availableCardWindow, self.availableCardWindow + 4):
                card_x = self.rightPanelX + self.availableCardSpacing
                card_y = self.rightPanelY + self.availableCardSpacing + (self.rightPanelY - self.availableCardSpacing*2 - 10)*(idx-self.availableCardWindow)
                scaled_image = pygame.transform.scale(card.image, (int(CARD_WIDTH * self.availableCardScale), int(CARD_HEIGHT * self.availableCardScale)))
                screen.blit(scaled_image, (card_x, card_y))
                screen.blit(gFont_list["default"].render( card.name, True, (0,0,0)),(card_x + 110, card_y + 10))
                screen.blit(gFont_list["small"].render( card.type, True, (0,0,0)),(card_x + 110, card_y + 40))
                screen.blit(gFont_list["small"].render( "ATK: "+str(card.attack)+" DEF: "+str(card.defense)+" Range: "+str(card.range_start)+"-"+str(card.range_end)+" SPD: "+str(card.speed), True, (0,0,0)),(card_x + 110, card_y+70))
        
        # render selected card detail
        if self.selectDeck and len(self.player.deck.card_deck) !=0 and self.deckIndex < len(self.player.deck.card_deck):
            card = self.player.deck.card_deck[self.deckIndex]
            screen.blit(card.image, (self.selectedCardSpacing, self.selectedCardSpacing))
            screen.blit(gFont_list["title"].render(card.name, True, (0,0,0)),(self.selectedCardSpacing , self.selectedCardSpacing + CARD_HEIGHT + 10))
            # screen.blit(gFont_list["header"].render("damage : " + str(card.attack), True, (0,0,0)),(self.selectedCardSpacing , self.selectedCardSpacing + CARD_HEIGHT + 50))
            # screen.blit(gFont_list["header"].render("range : " + str(card.range_end), True, (0,0,0)),(self.selectedCardSpacing , self.selectedCardSpacing + CARD_HEIGHT + 80))
            # screen.blit(gFont_list["header"].render("defend : " + str(card.defense), True, (0,0,0)),(self.selectedCardSpacing , self.selectedCardSpacing + CARD_HEIGHT + 110))
            # screen.blit(gFont_list["header"].render("speed : " + str(card.speed), True, (0,0,0)),(self.selectedCardSpacing , self.selectedCardSpacing + CARD_HEIGHT + 140))
            screen.blit(gFont_list["header"].render("description : " + card.description, True, (0,0,0)),(self.selectedCardSpacing , self.selectedCardSpacing + CARD_HEIGHT + 50))
            bold_font = gFont_list["header"]
            bold_font.set_bold(True)
            screen.blit(bold_font.render(str(card.attack), True, (0,0,0)), (self.selectedCardSpacing + 43, self.selectedCardSpacing +207))
            screen.blit(bold_font.render(str(card.defense), True, (0,0,0)), (self.selectedCardSpacing + 93, self.selectedCardSpacing +207))
            screen.blit(bold_font.render(str(card.range_end), True, (0,0,0)), (self.selectedCardSpacing + 143, self.selectedCardSpacing +207))
            screen.blit(bold_font.render(str(card.speed), True, (0,0,0)), (self.selectedCardSpacing + 170, self.selectedCardSpacing + 12))

    
        elif not self.selectDeck and len(self.availableCard)!=0 and self.availableCardIndex < len(self.availableCard):
            card = self.availableCard[self.availableCardIndex]
            screen.blit(card.image, (self.selectedCardSpacing, self.selectedCardSpacing))
            screen.blit(gFont_list["title"].render(card.name, True, (0,0,0)),(self.selectedCardSpacing , self.selectedCardSpacing + CARD_HEIGHT + 10))
            # screen.blit(gFont_list["header"].render("damage : " + str(card.attack), True, (0,0,0)),(self.selectedCardSpacing , self.selectedCardSpacing + CARD_HEIGHT + 50))
            # screen.blit(gFont_list["header"].render("range : " + str(card.range_end), True, (0,0,0)),(self.selectedCardSpacing , self.selectedCardSpacing + CARD_HEIGHT + 80))
            # screen.blit(gFont_list["header"].render("defend : " + str(card.defense), True, (0,0,0)),(self.selectedCardSpacing , self.selectedCardSpacing + CARD_HEIGHT + 110))
            # screen.blit(gFont_list["header"].render("speed : " + str(card.speed), True, (0,0,0)),(self.selectedCardSpacing , self.selectedCardSpacing + CARD_HEIGHT + 140))
            screen.blit(gFont_list["header"].render("description : " + card.description, True, (0,0,0)),(self.selectedCardSpacing , self.selectedCardSpacing + CARD_HEIGHT + 50))
            bold_font = gFont_list["header"]
            bold_font.set_bold(True)
            screen.blit(bold_font.render(str(card.attack), True, (0,0,0)), (self.selectedCardSpacing + 43, self.selectedCardSpacing +207))
            screen.blit(bold_font.render(str(card.defense), True, (0,0,0)), (self.selectedCardSpacing + 93, self.selectedCardSpacing +207))
            screen.blit(bold_font.render(str(card.range_end), True, (0,0,0)), (self.selectedCardSpacing + 143, self.selectedCardSpacing +207))
            screen.blit(bold_font.render(str(card.speed), True, (0,0,0)), (self.selectedCardSpacing + 170, self.selectedCardSpacing + 12))

        # render highlight for selection        
        if self.selectDeck:
            pygame.draw.rect(screen, (255,255,0), (self.middlePanelX + self.deckSpacing + (CARD_WIDTH*self.deckScale + self.deckSpacing)*(self.deckIndex%self.cardPerRow) , self.middlePanelY + self.deckSpacing+ (CARD_HEIGHT*self.deckScale + self.deckSpacing)*(self.deckIndex//self.cardPerRow), CARD_WIDTH*self.deckScale, CARD_HEIGHT*self.deckScale), 3)
        else:
            card_x = self.rightPanelX + self.availableCardSpacing
            card_y = self.rightPanelY + self.availableCardSpacing + (self.rightPanelY - self.availableCardSpacing*2 - 10)*((self.availableCardIndex- self.availableCardWindow%4)%4)
            pygame.draw.rect(screen, (255,255,0), (card_x, card_y , CARD_WIDTH* self.availableCardScale, CARD_HEIGHT* self.availableCardScale),3)

        # render deck and available card information
        screen.blit(gFont_list["header"].render(f"Deck {len(self.player.deck.card_deck)}/30", True, (0,0,0)),(self.rightPanelX - 120 , self.middlePanelY -60))
        screen.blit(gFont_list["header"].render(f"Available Cards {len(self.availableCard)}", True, (0,0,0)),(SCREEN_WIDTH - 190 , self.middlePanelY - 60))

        # render scroll wheel
        if len(self.availableCard) != 0:
            scroll_wheel_y = self.rightPanelY + ((SCREEN_HEIGHT*0.8-60)/len(self.availableCard) * self.availableCardWindow)
            pygame.draw.rect(screen, (100,100,100), (SCREEN_WIDTH * 0.98, scroll_wheel_y, SCREEN_WIDTH * 0.02, 60))

        # render filter button
        for button in self.effectButton:
            button.draw(screen)

        for button in self.typeButton:
            button.draw(screen)

        for button in self.classButton:
            button.draw(screen)
        
        # render filter description
        screen.blit(gFont_list["default"].render("Card Class", True, (0,0,0)),(self.topPanelX + 10, self.topPanelY))
        screen.blit(gFont_list["default"].render("Card Type", True, (0,0,0)),(self.topPanelX + 10, self.topPanelY + BUTTON_LOWER_OFFSET - 15))
        screen.blit(gFont_list["default"].render("Effect Type", True, (0,0,0)),(self.rightPanelX - 60, self.topPanelY))

        # render sort button
        self.sortButton.draw(screen)







class Button:
    def __init__(self, x, y, width, height, text=''):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (150, 150, 150)
        self.clicked_color = (100, 200, 100)
        self.hover_color = (100, 100, 50)
        self.text = text
        self.isClick = False
        self.font = gFont_list["small"]
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