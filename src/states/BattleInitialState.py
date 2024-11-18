from src.dependency import *
from src.constants import *
from src.battleSystem.Buff import *
from src.BattlePause import *
from src.Render import *
import pygame
import sys
import random

class BattleInitialState(BaseState):
    def __init__(self):
        super(BattleInitialState, self).__init__()
        self.dice = 1
        self.roll = False
        self.pauseHandler = BattlePauseHandler()

    def Enter(self, params):
        print("\n>>>>>> Enter BattleInitialState <<<<<<")
        self.params = params
        battle_param = self.params['battleSystem']
        self.player = battle_param['player']
        self.enemy = battle_param['enemy']
        self.field = battle_param['field']
        self.turn = battle_param['turn']
        self.currentTurnOwner = battle_param['currentTurnOwner']  

        # For setting up the initial position at the start of each battle
        self.player.move_to(self.field[self.player.fieldTile_index], self.field)
        self.enemy.move_to(self.field[self.enemy.fieldTile_index], self.field)

        self.dice = 1
        self.roll = False

        for card in self.player.cardsOnHand:
            print("Player's Hand Card: ", card.name)

        # Mock buff
        # mock_buff = Buff(CARD_BUFF["attack_boost"])
        # self.player.add_buff(mock_buff)
        print(f'Player Buffs: {self.player.buffs}')
        print(f'Enemy Buffs: {self.enemy.buffs}')

        # apply buff to all cards on hand
        self.player.apply_buffs_to_cardsOnHand()
        self.enemy.apply_buffs_to_cardsOnHand()
        
        self.pauseHandler.reset()

    def Exit(self):
        pass

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
                elif event.key == pygame.K_k:
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
                elif event.key == pygame.K_l:
                    self.winner = PlayerType.ENEMY
                    self.params['battleSystem'] = {
                        'player': self.player,
                        'enemy': self.enemy,
                        'field': self.field,
                        'turn': self.turn,
                        'currentTurnOwner': self.currentTurnOwner,
                        'winner': self.winner
                    }
                    g_state_manager.Change(BattleState.FINISH_PHASE, self.params)
                elif event.key == pygame.K_RETURN:
                    if self.roll == False and self.currentTurnOwner == PlayerType.PLAYER:
                        self.roll_dice()
                        self.roll = True
                    elif self.roll == True:
                        self.params['battleSystem'] = {
                            'player': self.player,
                            'enemy': self.enemy,
                            'field': self.field,
                            'turn': self.turn,
                            'currentTurnOwner': self.currentTurnOwner
                        }
                        g_state_manager.Change(BattleState.SELECTION_PHASE, self.params)
        
        if self.currentTurnOwner == PlayerType.ENEMY and self.roll == False:
            self.roll_dice()
            self.roll = True

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
        RenderTurn(screen, "battleInitial", self.turn, self.currentTurnOwner)
        RenderEntityStats(screen, self.player, self.enemy)
            
        # Title
        if self.roll:           
            if self.dice < 4:
                desc_1 = f'{self.currentTurnOwner.value} Got {DICE_ROLL_BUFF[self.dice - 1].name}'
            else:
                desc_1 = f'{self.currentTurnOwner.value} Got No Buff'
            desc_2 = "Press Enter to Start"
            RenderDescription(screen, desc_1, desc_2)
        else:
            RenderDescription(screen, "Press Enter to Roll the Dice")
             
        # Render cards on player's hand
        for order, card in enumerate(self.player.cardsOnHand):
            card.render(screen, order)

        # Render field
        for fieldTile in self.field:
            fieldTile.render(screen)
    
        # Render dice
        if not self.roll:
            screen.blit(gDice_image_list[f'dice_roll_{self.dice}'], (SCREEN_WIDTH//2 - 32, SCREEN_HEIGHT - HUD_HEIGHT - 74))
        else:
            screen.blit(gDice_image_list[f'dice_{self.dice}'], (SCREEN_WIDTH//2 - 32, SCREEN_HEIGHT - HUD_HEIGHT - 74))

        self.pauseHandler.render(screen)
        
    def roll_dice(self):
        # Play dice sound
        gSounds['dice_roll'].play()

        # Render dice rolling animation
        for _ in range(30):  # Increase the number of iterations for a smoother effect
            self.dice = random.randint(1, 6)  # Randomly change the dice number
            self.render(pygame.display.get_surface())  # Render the current state of the screen
            # screen = pygame.display.get_surface()
            # screen.blit(gDice_image_list[f'dice_roll_{self.dice}'], (SCREEN_WIDTH//2 - 32, SCREEN_HEIGHT - HUD_HEIGHT - 74))
            pygame.display.flip()  # Update the display to show changes
            pygame.time.delay(10)  # Delay to control the speed of dice rolling

        # Roll the dice and convert the value to buff
        final_number = self.dice
        self.dice_buff(final_number)

    def dice_buff(self, diceNumber):
        print(f'Dice Number: {diceNumber}')
        if diceNumber < 4:                      # 1, 2, 3
            buff = Buff(DICE_ROLL_BUFF[diceNumber - 1])   # Get the buff based on the dice number
            if self.currentTurnOwner == PlayerType.PLAYER:   
                self.player.add_buff(buff)
            elif self.currentTurnOwner == PlayerType.ENEMY:
                self.enemy.add_buff(buff)
        else:
            print('no buff')