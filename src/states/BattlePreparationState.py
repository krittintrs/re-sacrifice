import copy
from src.dependency import *
from src.constants import *
from src.battleSystem.battleEntity.Player import Player
from src.battleSystem.battleEntity.Enemy import Enemy
from src.battleSystem.Deck import Deck
from src.battleSystem.FieldTile import FieldTile
import pygame
import sys

class BattlePreparationState(BaseState):
    def __init__(self):
        super(BattlePreparationState, self).__init__()
        self.menu = ["Start Battle", "Edit deck", "Edit enemy deck"]
        self.selectIndex = 0

        # base turn
        self.turn = 1
        self.currentTurnOwner = PlayerType.PLAYER

        # Create field
        self.field = self.create_field(9)  # Create 9 field in a single row
    
    def mockDeck(self):
        deck = Deck()
        for i, card in enumerate(card_dict.values()):
            deck.addCard(card)
        return deck
    
    def initialDraw(self):
        self.player.deck.shuffle()
        self.player.cardsOnHand = self.player.deck.draw(5)
        self.enemy.deck.shuffle()
        self.enemy.cardsOnHand = self.enemy.deck.draw(5)

    def Enter(self, params):
        self.player = params['player']
        self.enemy = params['enemy']

        if self.player is None:
            # mock player
            self.player = Player("player")
            self.player.deck.read_conf(DECK_DEFS["default"], CARD_DEFS)

        if self.enemy is None:
            # mock enemy
            self.enemy = Enemy("enemy")  
            self.enemy.deck.read_conf(DECK_DEFS["default"], CARD_DEFS)

        #Set up the initial default position of player and enemy
        self.player.fieldTile_index  = 2
        self.enemy.fieldTile_index = 7

        if len(self.player.deck.card_deck) > 0:
            print('player deck size: ', len(self.player.deck.card_deck))
        else:
            print('player deck is None')
    
    def Exit(self):
        pass

    def update(self, dt, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.selectIndex = (self.selectIndex + 1)%len(self.menu)
                if event.key == pygame.K_LEFT:
                    self.selectIndex = (self.selectIndex - 1)%len(self.menu)
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_RETURN:
                    if self.selectIndex == 0:
                        self.initialDraw()
                        g_state_manager.Change(BattleState.INITIAL_PHASE, {
                            'player': self.player,
                            'enemy': self.enemy,
                            'field': self.field,
                            'turn': self.turn,
                            'currentTurnOwner': self.currentTurnOwner
                        })
                    elif self.selectIndex == 1:
                        g_state_manager.Change(BattleState.DECK_BUILDING, {
                            'player': self.player,
                            'enemy':self.enemy,
                            'edit_player_deck':True
                        })
                    else:
                        g_state_manager.Change(BattleState.DECK_BUILDING, {
                            'player': self.player,
                            'enemy':self.enemy,
                            'edit_player_deck':False
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
    
    def create_field(self, num_fieldTile):
        field = []
        for i in range(num_fieldTile):
            x = i * 100  # Adjust the x position based on index
            y = 200  # Since you have only one row, y is constant
            field.append(FieldTile(i, (x, y)))  # Create and append each fieldTile
        return field
