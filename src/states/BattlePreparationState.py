import copy
from src.battleSystem.battleEntity.Boss import Boss
from src.dependency import *
from src.constants import *
from src.battleSystem.battleEntity.Player import Player
from src.battleSystem.battleEntity.Enemy import Enemy
from src.battleSystem.Buff import Buff
from src.battleSystem.FieldTile import FieldTile
from src.Render import *
from src.battleSystem.battleEntity.entity_defs import *
from src.components.Selector import Selector
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

        # Create selector
        self.selectors = [
            Selector("start_battle", y=491, scale=1.0, center=True),
            Selector("edit_deck", y=556, scale=1.0, center=True),
            Selector("edit_opponent_deck", y=621, scale=1.0, center=True)
        ]

    def initialDraw(self):
        self.player.deck.shuffle()
        # for card in self.player.deck.card_deck:
        #     if card.name in ["Trap", "You shall not pass", "Long Range Attack", "Move 2", "Move 1"]:
        #         self.player.cardsOnHand.append(card)
        # for card in self.enemy.deck.card_deck:
        #     if card.name in ["Pull Attack", "Push Attack"]:
        #         self.enemy.cardsOnHand.append(card)
        # for card in self.player.deck.card_deck:
        #     if card.name in ["Long Range Attack", "Move 1"]:
        #         self.player.cardsOnHand.append(card)

        self.player.cardsOnHand = self.player.deck.draw(5)
        self.enemy.deck.shuffle()
        self.enemy.cardsOnHand = self.enemy.deck.draw(5)

        # self.player.add_buff(Buff(CARD_BUFF["attack_debuff"]))
        # self.player.add_buff(Buff(CARD_BUFF["defense_debuff"]))

    def Enter(self, params):
        print("Entering BattlePreparationState")
        play_music("battle_bgm")
        self.params = params
        battle_param = self.params['battleSystem']
        self.player = battle_param['player']
        self.enemy = battle_param['enemy']

        if 'rpg' not in self.params.keys():
            # mock player
            self.player = Player(BATTLE_ENTITY["default_warrior"])
            # mock enemy

            # self.enemy = Enemy(BATTLE_ENTITY["default_enemy"]) #choose type of enemy here
            self.enemy = Boss(BATTLE_ENTITY["default_enemy"])

        #Set up the initial default position of player and enemy
        self.player.fieldTile_index  = 2
        self.enemy.fieldTile_index = 7

        if len(self.player.deck.card_deck) > 0:
            print('player deck size: ', len(self.player.deck.card_deck))
        else:
            print('player deck is None')

        self.selected_index = 0

    def Exit(self):
        pass

    def update(self, dt, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                # Navigate using arrow keys
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.selected_index = (self.selected_index + 1) % len(self.selectors)
                elif event.key == pygame.K_UP:
                    self.selected_index = (self.selected_index - 1) % len(self.selectors)
                elif event.key == pygame.K_RETURN:
                    selected_selector = self.selectors[self.selected_index]
                    if selected_selector.name == "start_battle":
                        self.initialDraw()
                        self.params['battleSystem'] = {
                            'player': self.player,
                            'enemy': self.enemy,
                            'field': self.field,
                            'turn': self.turn,
                            'currentTurnOwner': self.currentTurnOwner
                        }
                        g_state_manager.Change(BattleState.INITIAL_PHASE, self.params)
                    elif selected_selector.name == "edit_deck":
                        self.params['battleSystem'] = {
                            'player': self.player,
                            'enemy': self.enemy,
                            'edit_player_deck': True,
                            'from_state': BattleState.PREPARATION_PHASE 
                        }
                        g_state_manager.Change(BattleState.DECK_BUILDING, self.params)    
                    elif selected_selector.name == "edit_opponent_deck":
                        self.params['battleSystem'] = {
                            'player': self.player,
                            'enemy': self.enemy,
                            'edit_player_deck': False,
                            'from_state': BattleState.PREPARATION_PHASE
                        }
                        g_state_manager.Change(BattleState.DECK_BUILDING, self.params)

        # Update selector
        for idx, selector in enumerate(self.selectors):
            selector.set_active(idx == self.selected_index)

        # Update buff
        for buff in self.player.buffs:
            buff.update(dt, events)
        for buff in self.enemy.buffs:
            buff.update(dt, events)
    
        self.player.update(dt)
        self.enemy.update(dt)

    def render(self, screen):
        RenderTurn(screen, "battleInitial", self.turn, self.currentTurnOwner)
        RenderEntityStats(screen, self.player, self.enemy)
             
        # Render selector
        for selector in self.selectors:
            selector.draw(screen)

        # Render cards on player's hand
        for order, card in enumerate(self.player.cardsOnHand):
            card.render(screen, order)

        # Render field
        for fieldTile in self.field:
            fieldTile.render(screen)
    
    def create_field(self, num_fieldTile):
        field = []
        start_x = (SCREEN_WIDTH - (num_fieldTile * FIELD_WIDTH + (num_fieldTile-1) * FIELD_GAP)) // 2
        for i in range(num_fieldTile + 1):
            x = start_x + (i * (FIELD_WIDTH + FIELD_GAP))
            y = FIELD_OFFSET_Y
            field.append(FieldTile(i, (x, y)))  # Create and append each fieldTile
        return field
