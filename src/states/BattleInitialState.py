from src.dependency import *
from src.constants import *
from src.battleSystem.FieldTile import FieldTile
from src.battleSystem.Buff import *
from src.Render import *
import pygame
import sys
import random

class BattleInitialState(BaseState):
    def __init__(self):
        super(BattleInitialState, self).__init__()
        self.dice = 0
        self.roll = False

    def Enter(self, params):
        print("\n>>>>>> Enter BattleInitialState <<<<<<")

        self.player = params['player']
        self.enemy = params['enemy']
        self.field = params['field']
        self.turn = params['turn']
        self.currentTurnOwner = params['currentTurnOwner']  

        # For setting up the initial position at the start of each battle
        self.player.move_to(self.field[self.player.fieldTile_index], self.field)
        self.enemy.move_to(self.field[self.enemy.fieldTile_index], self.field)

        self.dice = 0
        self.roll = False

        for card in self.player.cardsOnHand:
            print("Player's Hand Card: ", card.name)

        # Mock buff
        # mock_buff = Buff(BuffConf('bonus_attack', 1, [1, 0, 0, 0], 0, gBuffIcon_image_list['attack']))
        # self.player.add_buff(mock_buff)
        print(f'Player Buffs: {self.player.buffs}')
        print(f'Enemy Buffs: {self.enemy.buffs}')

        # apply buff to all cards on hand
        self.player.apply_buffs_to_cardsOnHand()
        self.enemy.apply_buffs_to_cardsOnHand()

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
                elif event.key == pygame.K_SPACE and self.roll == False and self.currentTurnOwner == PlayerType.PLAYER:
                    self.roll_dice()
                    self.roll = True
                elif event.key == pygame.K_RETURN and self.roll == True:
                    g_state_manager.Change(BattleState.SELECTION_PHASE, {
                        'player': self.player,
                        'enemy': self.enemy,
                        'field': self.field,
                        'turn': self.turn,
                        'currentTurnOwner': self.currentTurnOwner
                    })
        
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
        RenderTurn(screen, 'Initial State', self.turn, self.currentTurnOwner)
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
            RenderDescription(screen, "Press Spacebar to Roll the Dice")
             
        # Render cards on player's hand
        for order, card in enumerate(self.player.cardsOnHand):
            card.render(screen, order)

        # Render field
        for fieldTile in self.field:
            fieldTile.render(screen)
    
        # TODO: Render dice image
        pygame.draw.rect(screen, (255, 255, 255), (SCREEN_WIDTH//2 + 50, SCREEN_HEIGHT - HUD_HEIGHT - 40, 150, 40)) 
        screen.blit(pygame.font.Font(None, 36).render("Dice: " + str(self.dice), True, (0, 0, 0)), (SCREEN_WIDTH//2 + 50, SCREEN_HEIGHT - HUD_HEIGHT - 30))
    
    def roll_dice(self):
        # Play dice sound
        gSounds['dice_roll'].play()

        # Render dice rolling animation
        for _ in range(30):  # Increase the number of iterations for a smoother effect
            self.dice = random.randint(1, 6)  # Randomly change the dice number
            self.render(pygame.display.get_surface())  # Render the current state of the screen
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