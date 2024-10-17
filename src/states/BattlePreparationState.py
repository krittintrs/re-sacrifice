from src.dependency import *
from src.constants import *
from src.cardSystem.Entity import *
from src.cardSystem.Deck import Deck
import pygame
import sys

class BattlePreparationState(BaseState):
    def __init__(self):
        super(BattlePreparationState, self).__init__()
        self.menu = ["Start Battle", "Edit deck"]
        self.selectIndex = 0

        # base turn
        self.turn = 0
        self.currentTurnOwner = PlayerType.ENEMY
    
    def mockDeck(self):
        deck = Deck()
        for card in card_dict.values():
            deck.addCard(card)
        return deck

    def initialDraw(self):
        self.deck.shuffle()
        self.player.cardsOnHand = self.deck.draw(5)

    def Enter(self, params):
        self.deck = params['deck']
        self.player = params['player']
        self.enemy = params['enemy']

        # mock deck, player, enemy
        self.deck = self.mockDeck() 
        self.player = Player("player")    
        self.enemy = Enemy("enemy")  
    
    def Exit(self):
        pass

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
                        self.initialDraw()
                        g_state_manager.Change(BattleState.INITIAL_PHASE, {
                            'deck': self.deck,
                            'player': self.player,
                            'enemy': self.enemy,
                            'turn': self.turn,
                            'currentTurnOwner': self.currentTurnOwner
                        })
                    else:
                        g_state_manager.Change(BattleState.DECK_BUILDING, {
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
    
        # Render cards on player's hand
        for order, card in enumerate(self.player.cardsOnHand):
            card.render(screen, order)
            
