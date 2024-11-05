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
        mock_buff = Buff(BuffConf('bonus_attack', 1, [1, 0, 0, 0], sprite_collection['attack_icon']))
        self.player.add_buff(mock_buff)
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

    def render(self, screen):
        RenderTurn(screen, 'Initial State', self.turn, self.currentTurnOwner)
        RenderEntityStats(screen, self.player, self.enemy)
            
        # Title
        if self.roll:
            screen.blit(pygame.font.Font(None, 36).render("Cards:    Press Enter start", True, (255, 255, 255)), (10, SCREEN_HEIGHT - HUD_HEIGHT + 10))
            if self.dice < 4:
                text = f'{self.currentTurnOwner.value} got {DICE_ROLL_BUFF[self.dice - 1].name}'
            else:
                text = f'{self.currentTurnOwner.value} got No Buff'

            text_surface = pygame.font.Font(None, 36).render(text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - HUD_HEIGHT))

            # Draw the brown rectangle behind the text (with some padding)
            padding = 10
            pygame.draw.rect(screen, (139, 69, 19), (text_rect.x - padding, text_rect.y - padding,
                                                    text_rect.width + 2 * padding, text_rect.height + 2 * padding))

            # Blit the text surface on top of the rectangle
            screen.blit(text_surface, text_rect)
        else:
            screen.blit(pygame.font.Font(None, 36).render("Cards:    Press Spacebar to Roll the dice", True, (255, 255, 255)), (10, SCREEN_HEIGHT - HUD_HEIGHT + 10))   
        
        # Render cards on player's hand
        for order, card in enumerate(self.player.cardsOnHand):
            card.render(screen, order)

        # Render field
        for fieldTile in self.field:
            fieldTile.render(screen, len(self.field))
    
        # Clear only the dice result area (fill the area with the background color)
        pygame.draw.rect(screen, (255, 255, 255), (10, SCREEN_HEIGHT - HUD_HEIGHT - 40, 150, 40))  # Adjust size and position based on your layout

        # Render dice result
        screen.blit(pygame.font.Font(None, 36).render("Dice: " + str(self.dice), True, (0, 0, 0)), (10, SCREEN_HEIGHT - HUD_HEIGHT - 30))
    
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