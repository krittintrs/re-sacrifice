from src.states.BaseState import BaseState
from src.dependency import *
from src.constants import *
from src.BattlePause import *
from src.Render import *
import pygame
import sys

class BattleFinishState(BaseState):
    def __init__(self):
        super(BattleFinishState, self).__init__()
        self.pauseHandler = BattlePauseHandler()

    def Enter(self, params):
        print("\n>>>>>> Enter BattleFinishState <<<<<<")
        self.params = params
        battle_param = self.params['battleSystem']
        self.player = battle_param['player']
        self.enemy = battle_param['enemy']
        self.field = battle_param['field']
        self.turn = battle_param['turn']
        self.currentTurnOwner = battle_param['currentTurnOwner']  
        self.winner = battle_param['winner']  

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
                if event.key == pygame.K_RETURN:
                    self.player.reset_everything()
                    self.enemy.reset_everything()
                    for fieldtile in self.field:
                        fieldtile.remove_entity()
                        fieldtile.remove_second_entity()
                    
                    if 'rpg' in self.params.keys():
                        # TODO: entering RPG
                        if self.winner == PlayerType.PLAYER:
                            self.params['rpg']["win_battle"] = True
                        else:
                            self.params['rpg']["win_battle"] = False
                        self.params['rpg']["enter_battle"] = False
                        self.params['rpg']["exit_battle"] = True
                        self.params['bgm'] = 'battle'
                        if self.params['rpg']["map"] == "TOWN":
                            g_state_manager.Change(RPGState.TOWN, self.params)
                        elif self.params['rpg']["map"] == "TAVERN":
                            g_state_manager.Change(RPGState.TAVERN, self.params)
                        elif self.params['rpg']["map"] == "GOBLIN":
                            g_state_manager.Change(RPGState.GOBLIN, self.params)
                        elif self.params['rpg']["map"] == "INTRO":
                            g_state_manager.Change(RPGState.INTRO, self.params)
                    else:
                        g_state_manager.Change(BattleState.PREPARATION_PHASE, self.params)

        # Update buff
        for buff in self.player.buffs:
            buff.update(dt, events)
        for buff in self.enemy.buffs:
            buff.update(dt, events)
            
        self.player.update(dt)
        self.enemy.update(dt)

    def render(self, screen):
        RenderTurn(screen, "battleFinish", self.turn, self.currentTurnOwner)
        RenderEntityStats(screen, self.player, self.enemy)

        line1 = "Player wins!" if self.winner == PlayerType.PLAYER else "Enemy wins!"
        line2 = "Press Enter to continue"
        RenderDescription(screen, line1, line2)

        self.pauseHandler.render(screen)