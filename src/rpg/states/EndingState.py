import pygame
import sys
from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT
from src.resources import g_state_manager, play_music, gFont_list
from src.EnumResources import GameState
import cv2

class EndingState:
    def __init__(self):
        pygame.init()
        
        self.warrior_ending_videos = [
            cv2.VideoCapture("src/rpg/cutscene/WarriorCutsceneEnding1.mp4"),
            cv2.VideoCapture("src/rpg/cutscene/CutsceneEnding2.mp4"),
            cv2.VideoCapture("src/rpg/cutscene/CutsceneEnding3.mp4"),
        ]
        self.mage_ending_videos = [
            cv2.VideoCapture("src/rpg/cutscene/MageCutsceneEnding1.mp4"),
            cv2.VideoCapture("src/rpg/cutscene/CutsceneEnding2.mp4"),
            cv2.VideoCapture("src/rpg/cutscene/CutsceneEnding3.mp4"),
        ]
        self.ranger_ending_videos = [
            cv2.VideoCapture("src/rpg/cutscene/RangerCutsceneEnding1.mp4"),
            cv2.VideoCapture("src/rpg/cutscene/CutsceneEnding2.mp4"),
            cv2.VideoCapture("src/rpg/cutscene/CutsceneEnding3.mp4"),
        ]

        self.playing_cutscene = False
   
    def Enter(self, enter_params):
        play_music("ending_bgm")
        if enter_params:
            self.params = enter_params
        print("Entering Ending State")
        print(self.params," Ending")
        
        self.current_stage = "cutscene"  
        self.ending = self.params['rpg']['ending']
        self.player_class = self.params['class']

        # select class video
        if self.player_class == "Warrior":
            self.ending_videos = self.warrior_ending_videos
        elif self.player_class == "Mage":
            self.ending_videos = self.mage_ending_videos
        elif self.player_class == "Ranger":
            self.ending_videos = self.ranger_ending_videos

        # handle AI ending
        if self.ending > 3:
            self.current_stage = "ai"
        else:
            self.playing_cutscene = True

    def Exit(self):
        if self.playing_cutscene:
            for video in self.ending_videos:
                video.release()

    def update(self, dt, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if self.current_stage == "cutscene" and self.playing_cutscene:
                        print("Skip cutscene")
                        self.skip_cutscene()
                        self.current_stage = "text"
                    elif self.current_stage == "text" or self.current_stage == "ai":
                        g_state_manager.Change(GameState.TITLE, {})
        
        if self.current_stage == "cutscene":
            if not self.playing_cutscene:
                self.current_stage = "text"

    def skip_cutscene(self):
        self.playing_cutscene = False
        for video in self.ending_videos:
            video.release() # Release video resource
        
    def render_cutscene(self, screen, video):
        ret, frame = video.read()
        if ret:
            print(f"Rendering cutscene: {self.ending}")
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
            frame = cv2.flip(frame,flipCode=1)
            frame = pygame.surfarray.make_surface(frame)
            frame = pygame.transform.scale(frame, (SCREEN_WIDTH, SCREEN_HEIGHT))
            screen.blit(frame, (0, 0))
        else:
            print("Cutscene ended")
            self.skip_cutscene()  # End cutscene when the video is finished
   
    def render(self, screen):
        if self.current_stage == "cutscene":
            if self.playing_cutscene:
                self.render_cutscene(screen, self.ending_videos[self.ending - 1])
        elif self.current_stage == "text":
            screen.fill((0, 0, 0))
            text = "To be continued..."
            font = gFont_list["game_title"]
            text_surface = font.render(text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
            screen.blit(text_surface, text_rect)
        elif self.current_stage == "ai":
            screen.fill((0, 0, 0))
            text = "CONGRATULATIONS! YOU ESCAPE THE MATRIX"
            font = gFont_list["game_title"]
            text_surface = font.render(text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
            screen.blit(text_surface, text_rect)

            second_text = "(AI Ending)"
            font = gFont_list["title"]
            text_surface = font.render(second_text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 50))
            screen.blit(text_surface, text_rect)
        
