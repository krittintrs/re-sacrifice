import pygame
from src.constants import *
from src.resources import gBackground_image_list
from src.EnumResources import *

def RenderBackground(screen, bgstate):
    screen.blit(gBackground_image_list[bgstate], (0, 0))

def RenderTurn(screen, state, turn, currentTurnOwner):
    RenderBackground(screen, BackgroundState.BATTLE)
    screen.blit(pygame.font.Font(None, 36).render(f"{state} - Turn {turn} ({currentTurnOwner.value}'s turn)", True, (0, 0, 0)), (10, 10))   

def RenderEntityStats(screen, player, enemy):
    # Display player stats on the top left
    player_stats = [
        f"HP: {player.health}",
        f"ATK: {player.attack}",
        f"DEF: {player.defense}",
        f"Speed: {player.speed}"
    ]
    for i, stat in enumerate(player_stats):
        screen.blit(pygame.font.Font(None, 24).render(stat, True, (0, 0, 0)), (10, STATS_OFFSET + i * 20))

    # Display enemy stats on the top right
    enemy_stats = [
        f"HP: {enemy.health}",
        f"ATK: {enemy.attack}",
        f"DEF: {enemy.defense}",
        f"Speed: {enemy.speed}"
    ]
    for i, stat in enumerate(enemy_stats):
        screen.blit(pygame.font.Font(None, 24).render(stat, True, (255, 0, 0)), (SCREEN_WIDTH - 100, STATS_OFFSET + i * 20))
   
def RenderSelectedCard(screen, playerSelectedCard, enemySelectedCard):
    screen.blit(pygame.font.Font(None, 36).render("Player's", True, (255, 255, 255)), (50, SCREEN_HEIGHT - HUD_HEIGHT // 2 - 30))
    screen.blit(pygame.font.Font(None, 36).render("Card", True, (255, 255, 255)), (50, SCREEN_HEIGHT - HUD_HEIGHT // 2))

    screen.blit(pygame.font.Font(None, 36).render("Enemy's", True, (255, 255, 255)), (SCREEN_WIDTH - 150, SCREEN_HEIGHT - HUD_HEIGHT // 2 - 30))
    screen.blit(pygame.font.Font(None, 36).render("Card", True, (255, 255, 255)), (SCREEN_WIDTH - 150, SCREEN_HEIGHT - HUD_HEIGHT // 2))

    playerSelectedCard.render(screen, 0.5)
    enemySelectedCard.render(screen, 3.5)

def RenderCurrentAction(screen, effect, effectOwner):
    font = pygame.font.Font(None, 36)
    text = font.render(f"Current Action: {effect.type} ({effectOwner.value})", True, (0, 0, 0))
    
    # Calculate the position to center the text horizontally
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - HUD_HEIGHT - 50))
    
    # Blit the text to the screen
    screen.blit(text, text_rect)
