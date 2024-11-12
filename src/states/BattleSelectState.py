import pygame
import sys
from src.dependency import *
from src.Render import *

class BattleSelectState(BaseState):
    def __init__(self):
        super(BattleSelectState, self).__init__()
        self.selected_index = 0

    def Enter(self, params):
        print("\n>>>>>> Enter BattleSelectState <<<<<<")
        # Retrieve the cards, entities, and field from the parameter
        self.player = params['player']
        self.enemy = params['enemy']
        self.field = params['field']
        self.turn = params['turn']
        self.currentTurnOwner = params['currentTurnOwner']  

        self.player.cardsOnHand[self.selected_index].isSelected = True

        # For Debug Buffs
        print(f'Player Buffs: {self.player.buffs}')
        self.player.print_buffs()
        print(f'Enemy Buffs: {self.enemy.buffs}')
        self.enemy.print_buffs()

        # apply buff to all cards on hand
        self.player.apply_buffs_to_cardsOnHand()
        self.enemy.apply_buffs_to_cardsOnHand()

        self.player.ChangeAnimation("cast")

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
                if event.key == pygame.K_LEFT:
                    newIndex = (self.selected_index - 1) % len(self.player.cardsOnHand)
                    self.change_selection(newIndex)
                if event.key == pygame.K_RIGHT:
                    newIndex = (self.selected_index + 1) % len(self.player.cardsOnHand)
                    self.change_selection(newIndex)
                if event.key == pygame.K_RETURN:
                    selectedCard = self.player.cardsOnHand[self.selected_index]
                    self.player.select_card(selectedCard)
                    selectedCard.print_stats()
                    for card in self.player.cardsOnHand:
                        print(f'Player\'s Hand Card: {card.name}, isSelected: {card.isSelected}')
                    g_state_manager.Change(BattleState.ACTION_PHASE, {
                        'player': self.player,
                        'enemy': self.enemy,
                        'field': self.field,
                        'turn': self.turn,
                        'currentTurnOwner': self.currentTurnOwner,
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
        
    def change_selection(self, newIndex):
        self.player.cardsOnHand[self.selected_index].isSelected = False
        self.player.cardsOnHand[newIndex].isSelected = True
        self.selected_index = newIndex

    def render(self, screen):
        RenderTurn(screen, "battleSelect", self.turn, self.currentTurnOwner)
        RenderEntityStats(screen, self.player, self.enemy)
        RenderDescription(screen, "Select Card: Press Enter to Confirm")
        
        # Render cards on player's hand
        for order, card in enumerate(self.player.cardsOnHand):
            card.render(screen, order)

        # Render field
        for fieldTile in self.field:
            fieldTile.render(screen)

