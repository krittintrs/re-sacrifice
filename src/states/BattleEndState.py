from src.states.BaseState import BaseState
from src.dependency import *
from src.constants import *
from src.BattlePause import *
from src.Render import *
import pygame
import sys
import time

class BattleEndState(BaseState):
    def __init__(self):
        super(BattleEndState, self).__init__()
        self.pauseHandler = BattlePauseHandler()

    def Enter(self, params):
        print("\n>>>>>> Enter BattleEndState <<<<<<")
        self.params = params
        battle_param = self.params['battleSystem']
        self.player = battle_param['player']
        self.enemy = battle_param['enemy']
        self.field = battle_param['field']
        self.turn = battle_param['turn']
        self.currentTurnOwner = battle_param['currentTurnOwner']  

        self.player.remove_selected_card()
        self.enemy.remove_selected_card()

        # summon attack
        for tile in self.field:
            if tile.second_entity:
                tile.second_entity.bot_action(self.field)

        self.waiting_for_sound = False

        self.pauseHandler = BattlePauseHandler()
        
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
                if entity.type == PlayerType.ENEMY:
                    entity.ChangeAnimation("death")
                else:
                    entity.ChangeAnimation("knock_down")
                gSounds['attack'].play()
                print(f"{entity.name} receive {buff.dot_damage} damage from {buff.name}")


    def update(self, dt, events):
        if self.pauseHandler.is_paused():
            self.pauseHandler.update(dt, events, self.params)
            return
        
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.pauseHandler.pause_game()
                if event.key == pygame.K_RETURN and not self.waiting_for_sound:
                    self.resolve_dot_damage(self.player)
                    self.resolve_dot_damage(self.enemy)
                    if self.player.health > 0 and self.enemy.health > 0:
                        gSounds['draw_card'].play()
                        self.waiting_for_sound = True
                    else:
                        if self.player.health <= 0:
                            self.winner = PlayerType.ENEMY
                        elif self.enemy.health <= 0:
                            self.winner = PlayerType.PLAYER
                        self.params['battleSystem'] = {
                            'player': self.player,
                            'enemy': self.enemy,
                            'field': self.field,
                            'turn': self.turn,
                            'currentTurnOwner': self.currentTurnOwner,
                            'winner': self.winner
                        }
                        g_state_manager.Change(BattleState.FINISH_PHASE, self.params)
                    
        if self.waiting_for_sound and not pygame.mixer.get_busy():
            self.next_turn()
            self.params['battleSystem'] = {
                'player': self.player,
                'enemy': self.enemy,
                'field': self.field,
                'turn': self.turn,
                'currentTurnOwner': self.currentTurnOwner
            }
            g_state_manager.Change(BattleState.INITIAL_PHASE, self.params)

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
        RenderTurn(screen, "battleEnd", self.turn, self.currentTurnOwner)
        RenderEntityStats(screen, self.player, self.enemy)
        RenderDescription(screen, "End Action: Press Enter to Draw New Card")
        
        # Render cards on player's hand
        for order, card in enumerate(self.player.cardsOnHand):
            card.render(screen, order)

        # Render field
        for fieldTile in self.field:
            fieldTile.render(screen)

        self.pauseHandler.render(screen)        