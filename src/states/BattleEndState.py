from src.states.BaseState import BaseState
from src.dependency import *
from src.constants import *
from src.Render import *
import pygame
import sys

class BattleEndState(BaseState):
    def __init__(self):
        super(BattleEndState, self).__init__()

    def Enter(self, params):
        print("\n>>>>>> Enter BattleEndState <<<<<<")
        self.player = params['player']
        self.enemy = params['enemy']
        self.field = params['field']
        self.turn = params['turn']
        self.currentTurnOwner = params['currentTurnOwner']  

        self.player.remove_selected_card()
        self.enemy.remove_selected_card()
        
    def next_turn(self):
        # Change turn owner
        if self.currentTurnOwner == PlayerType.PLAYER:
            self.currentTurnOwner = PlayerType.ENEMY
        else:
            self.currentTurnOwner = PlayerType.PLAYER

        # Increment turn
        self.turn += 1

        # Turn Pass Entity
        self.player.next_turn()
        self.enemy.next_turn()

    def Exit(self):
        pass

    def update(self, dt, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_SPACE:
                    pass
                if event.key == pygame.K_RETURN:
                    self.next_turn()
                    g_state_manager.Change(BattleState.INITIAL_PHASE, {
                        'player': self.player,
                        'enemy': self.enemy,
                        'field': self.field,
                        'turn': self.turn,
                        'currentTurnOwner': self.currentTurnOwner
                    })

        # Update buff
        for buff in self.player.buffs:
            buff.update(dt, events)
        for buff in self.enemy.buffs:
            buff.update(dt, events)

        self.player.update(dt)
        self.enemy.update(dt)

    def render(self, screen):
        RenderTurn(screen, 'End State', self.turn, self.currentTurnOwner)
        RenderEntityStats(screen, self.player, self.enemy)

        screen.blit(pygame.font.Font(None, 36).render("End Action: Press Enter to Draw New Card", True, (255, 255, 255)), (10, SCREEN_HEIGHT - HUD_HEIGHT + 10))   

        # Render cards on player's hand
        for order, card in enumerate(self.player.cardsOnHand):
            card.render(screen, order)

        # Render field
        for fieldTile in self.field:
            fieldTile.render(screen)


        