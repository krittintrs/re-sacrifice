from src.states.BaseState import BaseState
from src.dependency import *
from src.constants import *
from src.Render import *
import pygame
import sys
import time

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
        for tile in self.field:
            if tile.is_second_entity():
                if tile.second_entity.next_turn():
                    tile.second_entity.ChangeAnimation('death')
                    tile.remove_second_entity()



    def Exit(self):
        pass

    def resolve_dot_damage(self, entity):
        for buff in entity.buffs:
            entity.health += buff.dot_damage
            if buff.dot_damage > 0:
                print(f"{entity.name} receive {buff.dot_damage} health from {buff.name}")
            elif buff.dot_damage < 0:
                self.enemy.ChangeAnimation("death")
                gSounds['attack'].play()
                print(f"{entity.name} receive {buff.dot_damage} damage from {buff.name}")


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
                    self.resolve_dot_damage(self.player)
                    self.resolve_dot_damage(self.enemy)
                    if self.player.health > 0 and self.enemy.health > 0:
                        self.next_turn()
                        g_state_manager.Change(BattleState.INITIAL_PHASE, {
                            'player': self.player,
                            'enemy': self.enemy,
                            'field': self.field,
                            'turn': self.turn,
                            'currentTurnOwner': self.currentTurnOwner
                        })
                    else:
                        if self.player.health <= 0:
                            self.winner = PlayerType.ENEMY
                        elif self.enemy.health <= 0:
                            self.winner = PlayerType.PLAYER
                        g_state_manager.Change(BattleState.FINISH_PHASE, {
                            'player': self.player,
                            'enemy': self.enemy,
                            'field': self.field,
                            'turn': self.turn,
                            'currentTurnOwner': self.currentTurnOwner,
                            'winner': self.winner
                        })
                    

        # Update buff
        for buff in self.player.buffs:
            buff.update(dt, events)
        for buff in self.enemy.buffs:
            buff.update(dt, events)

        self.player.update(dt)
        self.enemy.update(dt)

        for tile in self.field:
            if tile.second_entity:
                tile.second_entity.update(dt)
            elif tile.is_occupied() and tile.entity.type == None:
                tile.entity.update(dt)

        self.remove_timeout_entity()

    def remove_timeout_entity(self):
        for tile in self.field:
            if tile.is_second_entity():
                if tile.second_entity.duration == 0:
                    print("remove second entity for timeout ", tile.index)
                    tile.remove_second_entity()

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


        