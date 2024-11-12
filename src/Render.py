import pygame
from src.constants import *
from src.resources import *
from src.EnumResources import *

def RenderBackground(screen, bgstate):
    screen.blit(gBackground_image_list[bgstate], (0, 0))

def RenderTurn(screen, state, turn, currentTurnOwner):
    RenderBackground(screen, BackgroundState.BATTLE)

    title_text = gFont_list["title"].render(f"{state} - Turn {turn} ({currentTurnOwner.value}'s turn)", True, (255, 255, 255))
    _, title_text_height = title_text.get_size()
    title_text_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, title_text_height // 2))
    screen.blit(title_text, title_text_rect)
    
    try:
        state_type = BattleState(state)
    except ValueError:
        try:
            state_type = SelectionState(state)
        except ValueError:
            state_type = None
            
    if state_type == BattleState.INITIAL_PHASE:
        clock = gClock_image_list["clock_0"]
    elif state_type == BattleState.SELECTION_PHASE:
        clock = gClock_image_list["clock_3"]
    elif state_type in [BattleState.ACTION_PHASE, BattleState.RESOLVE_PHASE] or state_type in list(SelectionState):
        clock = gClock_image_list["clock_6"]
    elif state_type == BattleState.END_PHASE:
        clock = gClock_image_list["clock_9"]
    else:
        clock = gClock_image_list["clock_0"]
    screen.blit(clock, (SCREEN_WIDTH // 2 - 61, 0))

def RenderEntityStats(screen, player, enemy):
    # Display player stats on the top left
    screen.blit(gFont_list["header"].render("Player Stats", True, (0, 0, 0)), (STATS_OFFSET_X, STATS_OFFSET_Y - 30))
    player_stats = [
        f"HP: {player.health}",
        f"ATK: {player.attack}",
        f"DEF: {player.defense}",
        f"Speed: {player.speed}"
    ]
    for i, stat in enumerate(player_stats):
        screen.blit(gFont_list["default"].render(stat, True, (0, 0, 0)), (STATS_OFFSET_X, STATS_OFFSET_Y + i * 15))

    # Display enemy stats on the top right
    enemy_stat_title_surface = gFont_list["header"].render("Enemy Stats", True, (0, 0, 0))
    enemy_stat_title_width, _ = enemy_stat_title_surface.get_size()
    screen.blit(enemy_stat_title_surface, (SCREEN_WIDTH - STATS_OFFSET_X - enemy_stat_title_width, STATS_OFFSET_Y - 30))
    enemy_stats = [
        f"HP: {enemy.health}",
        f"ATK: {enemy.attack}",
        f"DEF: {enemy.defense}",
        f"Speed: {enemy.speed}"
    ]
    for i, stat in enumerate(enemy_stats):
        stat_surface = gFont_list["default"].render(stat, True, (0, 0, 0))
        stat_width, _ = stat_surface.get_size()
        screen.blit(stat_surface, (SCREEN_WIDTH - STATS_OFFSET_X - stat_width, STATS_OFFSET_Y + i * 15))
   
def RenderSelectedCard(screen, playerSelectedCard, enemySelectedCard):
    screen.blit(gFont_list["title"].render("Player's", True, (255, 255, 255)), (50, SCREEN_HEIGHT - HUD_HEIGHT // 2 - 30))
    screen.blit(gFont_list["title"].render("Card", True, (255, 255, 255)), (50, SCREEN_HEIGHT - HUD_HEIGHT // 2))

    screen.blit(gFont_list["title"].render("Enemy's", True, (255, 255, 255)), (SCREEN_WIDTH - 150, SCREEN_HEIGHT - HUD_HEIGHT // 2 - 30))
    screen.blit(gFont_list["title"].render("Card", True, (255, 255, 255)), (SCREEN_WIDTH - 150, SCREEN_HEIGHT - HUD_HEIGHT // 2))

    playerSelectedCard.render(screen, 0.5)
    enemySelectedCard.render(screen, 3.5)

def RenderDescription(screen, line_1, line_2=None):
    text_1 = gFont_list["title"].render(line_1, True, (0, 0, 0))
    text_2 = gFont_list["title"].render(line_2, True, (0, 0, 0))
    
    screen.blit(text_1, (DESCRIPTION_OFFSET_X, DESCRIPTION_OFFSET_Y))
    screen.blit(text_2, (DESCRIPTION_OFFSET_X, DESCRIPTION_OFFSET_Y + 30))

def RenderFieldSelection(screen, field, availableTile, selectTile, effectOwner):
    for fieldTile in field:            
        if fieldTile.index in set(availableTile):
            fieldTile.image = gField_image_list[f"{effectOwner.value}_available"]
        else:
            fieldTile.image = gField_image_list["normal"]
        if selectTile>=0:
            if fieldTile.index == availableTile[selectTile]:
                fieldTile.image = gField_image_list[f"{effectOwner.value}_current"]
            
        fieldTile.render(screen)
        fieldTile.image = gField_image_list["normal"]
