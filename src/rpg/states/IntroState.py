import random
import sys
import time
import pygame
from src.battleSystem.deck_defs import DECK_DEFS
from src.rpg.entity.playerState.PlayerIdleState import PlayerIdleState
from src.rpg.entity.playerState.PlayerWalkState import PlayerWalkState
from src.rpg.EntityDefs import ENTITY_DEFS
from src.rpg.Player import Player
from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT
from src.rpg.StateMachine import StateMachine
import google.generativeai as genai
from src.rpg.NPC import NPC
from src.rpg.Prompts import *
from src.resources import g_state_manager, play_music
from src.EnumResources import RPGState,BattleState
from src.resources import gFont_list
from src.rpg.Utils import render_quests, render_dialogue
from src.battleSystem.battleEntity.Enemy import Enemy as BattleEnemy
from src.battleSystem.battleEntity.entity_defs import BATTLE_ENTITY
genai.configure(api_key="AIzaSyAbw1QNIQlmYgTYdsgLiOELef10E-M6BJY")
# Create the model


class IntroState:
    def __init__(self):
        pygame.init()
        
        self.scale_factor = 1.5
        self.current_stateIndex = 0
        
        # Initialize map
        self.map_surface = pygame.image.load("src/rpg/sprite/map/IntroMap.jpg")
        self.map_surface = pygame.transform.scale(self.map_surface, (SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Initialize NPCs with unique prompts
        self.npcs = [
            NPC("God", 631, 489, "src/rpg/sprite/NPC/God_Godoftime", PROMPTS['God'],'down',self.scale_factor, DEFAULT_TEXT["God"])
            # Add more NPCs here
        ]

        # Initial Tutorial
        self.battle_images = []
        for i in range(1,8):
            image = pygame.image.load(f"src/rpg/sprite/Tutorial/Battle_{i}.png")
            image = pygame.transform.smoothscale(image, (SCREEN_WIDTH, SCREEN_HEIGHT))
            self.battle_images.append(image)

        # Dialogue state
        self.current_state = ""
        self.show_dialogue = False
        self.dialogue_text = ""
        self.player_input = ""
        self.response_button_rect = pygame.Rect(950, 470, 125, 40)
        self.close_button_rect = pygame.Rect(1100, 470, 125, 40)
        self.current_npc = None
        self.selected_option = 0

        self.last_blink_time = 0
        self.blink = False
        
        self.entering_battle = False        
        
        self.params = None 
        self.buildings = []
        self.building_interactions = {
            "warp_door": self.interact_with_warp_door,
        }
        self.generate_buildings()  # Add buildings with invisible walls
        self.quests = {}
        self.topics = {}

    def Enter(self, enter_params):
        self.params = enter_params
        self.player = enter_params['rpg']['rpg_player']
        print(self.player.x)
        print(self.player.y)
        print(self.params," TownMap")

        if 'bgm' not in self.params.keys():
            play_music("intro_bgm")
        else:
            if self.params['bgm'] != 'intro_bgm':
                play_music("intro_bgm")
        
        print("Entering RPG Start State")
        
    def add_invisible_wall(self, building_id, x1, y1, x2, y2):
        wall_rect = pygame.Rect(x1, y1, x2 - x1, y2 - y1)
        self.buildings.append({'id': building_id, 'rect': wall_rect, 'interacted': False})
    
    def remove_building_by_id(self, building_id):
        self.buildings = [building for building in self.buildings if building['id'] != building_id]
    
    def interact_with_warp_door(self):
        self.params['rpg']['rpg_player'].x = 627
        self.params['rpg']['rpg_player'].y = 580
        g_state_manager.Change(RPGState.TOWN, self.params)
    
    def generate_buildings(self):
        #Walls
        self.add_invisible_wall("wall1", 556, 202, 583, 719)
        self.add_invisible_wall("wall2", 698, 203, 714, 717)
        self.add_invisible_wall("wall3", 502, 3, 533, 203)
        self.add_invisible_wall("wall4", 748, 8, 772, 199)
        self.add_invisible_wall("wall5", 502, 197, 580, 219)
        self.add_invisible_wall("wall6", 699, 203, 771, 228)
        self.add_invisible_wall("wall7", 578, 700, 706, 711)
        # self.add_invisible_wall("wall8", 560, 500, 620, 530)
        # self.add_invisible_wall("wall9", 640, 500, 700, 530)
        #Door
        self.add_invisible_wall("warp_door", 526, 9, 766, 34)
        self.add_invisible_wall("door", 526, 39, 766, 64)
        
    def interact_with_npc(self, npc):
        # Calculate direction to face player and update NPC sprite
        npc.face_player(self.player.x, self.player.y)
        
        self.current_npc = npc
        self.show_dialogue = True
        self.dialogue_text = npc.dialogue_text or npc.default_text

    def wrap_text(self, text, font, max_width):
        # Split text into lines based on width constraints
        words = text.split()
        lines = []
        current_line = ""
        
        for word in words:
            # Test adding this word to the current line
            test_line = f"{current_line} {word}".strip()
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word

        # Append any remaining text to lines
        if current_line:
            lines.append(current_line)
        
        return lines

    def update_story(self):
        if self.current_npc:
            if self.current_npc.choice == -1:
                self.entering_battle = True
                pygame.event.get()
                keys = pygame.key.get_pressed()
                if keys:
                    # TODO: ending 4 (AI)
                    print("ending 4")
                    self.params['rpg']['ending'] = 4
                    g_state_manager.Change(RPGState.ENDING, self.params)
                    
            if self.current_npc.choice == 1:
                    print("enter battle")
                    self.entering_battle = True
                    pygame.event.get()
                    keys = pygame.key.get_pressed()  # Get current key states
                    if keys[pygame.K_RETURN]:  # Check if Enter key is pressed
                        self.current_state = "Fight_Intro"
                        self.show_dialogue = False
                        self.current_npc.choice = 0
                        
                        
            if self.current_state == "Finished_Fight_Intro" and not self.params['rpg']["enter_battle"]:
                self.current_npc.choice = 0
                print("enter battle enter")
                self.params['rpg']["enter_battle"] = True
                self.params['rpg']["map"] = "INTRO"
                self.params['battleSystem'] = {
                    'player': self.player.battlePlayer,
                    'enemy': BattleEnemy(BATTLE_ENTITY["default_enemy"])
                }
                self.entering_battle = False
                self.current_state = "Finished_Fight"
                g_state_manager.Change(BattleState.PREPARATION_PHASE, self.params)
                
            elif self.params['rpg']["exit_battle"]:
                self.params['rpg']["exit_battle"] = False
                if self.params['rpg']['win_battle']:
                    self.params['rpg']['inventory']['Gold'] += random.randint(70,90)
                    self.dialogue_text = self.current_npc.get_dialogue("{The player won the fight against the goblins and you will say to the player that when win a combat the player get some golds and a card as a reward and also tell the player they need to head to town just head north and don't forget to press space to interact}") 
                    card_list=[]
                    for card in DECK_DEFS[self.player.battlePlayer.job.value.lower()].card_dict:
                        if card["quantity"] != 0:
                            card_list.append(card["name"])
                    for i in range(1):
                        card_name = random.choice(card_list)
                        self.player.battlePlayer.deck.addCardInventory(card_name)
                        print("add card ", card_name, "to player inventory")
                    self.buildings = [b for b in self.buildings if b['id'] != "door"]
                else:
                    self.dialogue_text = self.current_npc.get_dialogue("{The player lost fight against the goblins, give the player another try}") 
              
    def update(self, dt, events):
        # Handle events
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.show_dialogue:
                        self.show_dialogue = False
                    else:
                        pygame.quit()
                        sys.exit()
                elif event.key == pygame.K_RETURN and not self.show_dialogue:
                    self.handle_enter()
                elif event.key == pygame.K_LEFT and not self.show_dialogue:
                    self.hangle_arrow("left")
                elif event.key == pygame.K_RIGHT and not self.show_dialogue:
                    self.hangle_arrow("right")
                elif event.key == pygame.K_RETURN and self.show_dialogue and not self.entering_battle:
                    # Handle Enter key to send response
                    if not self.player_input:
                        self.player_input = "continue"  # Default to "continue" if input is empty
                    self.dialogue_text = self.current_npc.get_dialogue(self.player_input)
                    self.player_input = ""  # Clear player input after sending

                    # Print or display the player's selected choice
                    print(f"Player choice: {self.current_npc.choice}")
                elif event.key == pygame.K_BACKSPACE and self.show_dialogue:
                    # Handle backspace for text input
                    self.player_input = self.player_input[:-1]
                
                elif event.unicode and self.show_dialogue:
                    # Append typed characters to player input
                    self.player_input += event.unicode
                
                else:
                    if event.key == pygame.K_SPACE:
                        for building in self.buildings:
                            # Check if player is within 5 pixels of the building
                            if self.player.Collides(building['rect'].inflate(10, 10)):  # Inflate rect by 5 pixels in each direction
                                building['interacted'] = True
                                building_id = building['id']
                                if building_id in self.building_interactions:
                                    self.building_interactions[building_id]()  # Call the unique interaction function
                        for npc in self.npcs:
                            npc_rect = npc.get_rect()
                            if self.player.Collides(npc_rect.inflate(10,10)):
                                print(f"interact with npc {npc.name}")
                                self.interact_with_npc(npc)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.show_dialogue:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.response_button_rect.collidepoint(mouse_pos):
                        print(self.player_input)
                        self.dialogue_text = self.current_npc.get_dialogue(self.player_input)
                        self.player_input = ""  # Clear player input

                        # Print or display the player's selected choice
                        print(f"Player choice: {self.current_npc.choice}")

                    elif self.close_button_rect.collidepoint(mouse_pos):
                        # Close dialogue box
                        self.show_dialogue = False
                mouse_x, mouse_y = pygame.mouse.get_pos()
                print(f"Mouse clicked at: ({mouse_x}, {mouse_y})")

        # Store original player position to revert if collision occurs
        original_x, original_y = self.player.x, self.player.y

        # Handle player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.player.MoveY(-self.player.walk_speed * dt)
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.player.MoveY(self.player.walk_speed * dt)
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.player.MoveX(-self.player.walk_speed * dt)
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.player.MoveX(self.player.walk_speed * dt)
        
        # Check for collisions with each building and revert to original position if collided
        for building in self.buildings:
            if self.player.Collides(building['rect']):
                self.player.ChangeCoord(original_x, original_y)  # Revert position
                break
        for npc in self.npcs:
            npc_rect = npc.get_rect()
            in_dialogue = self.show_dialogue and self.current_npc == npc
            npc.update(in_dialogue)
            if self.player.Collides(npc_rect):
                self.player.ChangeCoord(original_x, original_y)  # Revert position
                break
            
        # Update player animations
        self.player.update(dt, events)

        self.update_story()

    def render(self, screen):
        # Draw map
        screen.blit(self.map_surface, (0, 0))

        # Draw invisible walls as green rectangles for debugging
        # for building in self.buildings:
        #     pygame.draw.rect(screen, (0, 255, 0), building['rect'], 2)
            
        for npc in self.npcs:
            screen.blit(npc.image, (npc.x, npc.y))  # Render each NPC at its coordinates
                       
        # Render player
        self.player.render(screen)
        
        # Render the quest tracker on top-right
        render_quests(screen, self.quests)
        
        # Render any active dialogue
        if self.show_dialogue:
            render_dialogue(screen, self.current_npc, self.dialogue_text, self.blink, self.last_blink_time, self.player_input)

        if self.current_state == "Fight_Intro":
            screen.blit(self.battle_images[self.current_stateIndex], (0, 0))
    
    def handle_enter(self):
        if self.current_state == "Fight_Intro":
            if self.current_stateIndex < len(self.battle_images) - 1:
                self.current_stateIndex += 1
            else:
                self.current_stateIndex = 0
                self.current_state = "Finished_Fight_Intro"
                self.update_story()
    
    def hangle_arrow(self, direction):
        if self.current_state == "Fight_Intro":
            if direction == "left":
                if self.current_stateIndex > 0:
                    self.current_stateIndex -= 1
            elif direction == "right":
                if self.current_stateIndex < len(self.battle_images) - 1:
                    self.current_stateIndex += 1
                else:
                    self.current_stateIndex = 0
                    self.current_state = "Finished_Fight_Intro"
                    self.update_story()
    
    def Exit(self):
        pass
