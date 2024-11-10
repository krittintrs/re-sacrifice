import copy
from src.dependency import *
from src.constants import *
from src.battleSystem.battleEntity.Player import Player
from src.battleSystem.battleEntity.Enemy import Enemy
from src.battleSystem.Buff import Buff
from src.battleSystem.FieldTile import FieldTile
import pygame
import sys
import math

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
    
    def initialDraw(self):
        self.player.deck.shuffle()
        for card in self.player.deck.card_deck:
            if card.name in ["Trap", "You shall not pass", "Attack Summon", "Move 2", "Move 1"]:
                self.player.cardsOnHand.append(card)

        # self.player.cardsOnHand = self.player.deck.draw(5)
        self.enemy.deck.shuffle()
        self.enemy.cardsOnHand = self.enemy.deck.draw(5)

        # self.player.add_buff(Buff(CARD_BUFF["attack_debuff"]))
        # self.player.add_buff(Buff(CARD_BUFF["defense_debuff"]))

    def Enter(self, params):
        self.player = params['player']
        self.enemy = params['enemy']

        if self.player is None:
            # mock player class
            # job = PlayerClass.WARRIOR
            job = PlayerClass.MAGE
            gPlayer_animation_list = gMage_animation_list
            # mock player
            self.player = Player("player", job, gPlayer_animation_list)
            self.player.deck.read_conf(DECK_DEFS["default"], CARD_DEFS)

        if self.enemy is None:
            # mock enemy
            self.enemy = Enemy("enemy", gNormalGoblin_animation_list)
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

        # Update buff
        for buff in self.player.buffs:
            buff.update(dt, events)
        for buff in self.enemy.buffs:
            buff.update(dt, events)
    
        self.player.update(dt)
        self.enemy.update(dt)

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
        start_x = (SCREEN_WIDTH - (num_fieldTile * FIELD_WIDTH + (num_fieldTile-1) * FIELD_GAP)) // 2
        for i in range(num_fieldTile + 1):
            x = start_x + (i * (FIELD_WIDTH + FIELD_GAP))
            y = SCREEN_HEIGHT // 3 - FIELD_HEIGHT // 2
            print(f'x: {x}, y: {y}')
            field.append(FieldTile(i, (x, y)))  # Create and append each fieldTile
        return field
