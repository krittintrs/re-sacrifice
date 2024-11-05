import sys
import time
import pygame
from src.rpg.states.TavernMapState import TavernMapState
from src.rpg.entity.playerState.PlayerIdleState import PlayerIdleState
from src.rpg.entity.playerState.PlayerWalkState import PlayerWalkState
from src.rpg.EntityDefs import ENTITY_DEFS
from src.rpg.Player import Player
from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT
from src.rpg.StateMachine import StateMachine
import os
import google.generativeai as genai
import json
import re
from src.rpg.NPC import NPC
from src.rpg.Prompts import *
from src.resources import g_state_manager
from src.EnumResources import RPGState

genai.configure(api_key="AIzaSyAbw1QNIQlmYgTYdsgLiOELef10E-M6BJY")
# Create the model


class RPGStartState:
    def __init__(self):
        pygame.init()
        
        self.scale_factor = 1.5
        #  # Initialize the current state to this state
        # self.current_state = self
        # self.tavern_map_state = TavernMapState()
        
        # Initialize map
        self.map_surface = pygame.image.load("src/rpg/sprite/map/TownMap.jpg")
        self.map_surface = pygame.transform.scale(self.map_surface, (SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Initialize NPCs with unique prompts
        self.npcs = [
            NPC("Jim", 411, 453, "src/rpg/sprite/NPC/Jim_GoblinHunter", PROMPTS['Jim'],'right',self.scale_factor)
            # Add more NPCs here
        ]

        # Dialogue state
        self.show_dialogue = False
        self.dialogue_text = ""
        self.player_input = ""
        self.response_button_rect = pygame.Rect(950, 470, 125, 40)
        self.close_button_rect = pygame.Rect(1100, 470, 125, 40)
        self.current_npc = None
        self.selected_option = 0

        self.last_blink_time = 0
        self.blink = False
        
        # # Player and State Initialization
        # # Initialize player configuration
        player_conf = ENTITY_DEFS['player']
        self.player = Player(player_conf)
        self.player.x = SCREEN_WIDTH // 2 - self.player.width // 2
        self.player.y = SCREEN_HEIGHT // 2 - self.player.height // 2

        self.player.state_machine = StateMachine()
        self.player.state_machine.SetScreen(pygame.display.get_surface())
        self.player.state_machine.SetStates({
            'walk': PlayerWalkState(self.player),
            'idle': PlayerIdleState(self.player)
        })
        self.player.ChangeState('idle')  # Start in idle state
                
        self.params = None #{"player" : self.player, "story_checkpoint" : {"Gate_Open" : False} ,'Money': None, 'Inventory': None,'deck': None,'player': None,'enemy': None}
        # Initialize buildings and interactions
        self.buildings = []
        self.building_interactions = {
            "blacksmith_building": self.interact_with_building_1,
            "tavern_building": self.interact_with_tavern,
            # "John_npc": lambda: self.interact_with_npc("John", "Hello, traveler! I am John, the town's guide.")
        }
        self.generate_buildings()  # Add buildings with invisible walls
        self.quests = {} 
        self.topics = {}

    def Enter(self, enter_params):
        self.params = enter_params
        self.player = enter_params['rpg_player']
        print(self.params," TownMap")
        
        print("Entering RPG Start State")
        
    def add_invisible_wall(self, building_id, x1, y1, x2, y2):
        wall_rect = pygame.Rect(x1, y1, x2 - x1, y2 - y1)
        self.buildings.append({'id': building_id, 'rect': wall_rect, 'interacted': False})
    
    def remove_building_by_id(self, building_id):
        self.buildings = [building for building in self.buildings if building['id'] != building_id]
    
    def generate_buildings(self):
        #Buildings
        self.add_invisible_wall("blacksmith_building", 177, 130, 437, 258)
        self.add_invisible_wall("tavern_building", 510, 120, 760, 295)
        self.add_invisible_wall("market1_building", 922, 90, 1106, 246)
        self.add_invisible_wall("market2_building", 867, 262, 1047, 368)
        self.add_invisible_wall("residence_building", 846, 442, 1115, 558)
        self.add_invisible_wall("store_building", 509, 437, 766, 590)
        #Walls
        self.add_invisible_wall("south_wall", 48, 640, 1227, 676)
        self.add_invisible_wall("west_wall", 37, 51, 91, 629)
        self.add_invisible_wall("north_wall1", 94, 34, 598, 72)
        self.add_invisible_wall("north_wall2", 676, 34, 1239, 72)
        self.add_invisible_wall("guard_door", 587, 47, 688, 67)
        self.add_invisible_wall("east_wall", 1188, 56, 1240, 634)
        
        # #NPC
        # self.add_invisible_wall("John_npc", 411, 453, 440, 480)
        
    # Unique interaction functions for each building
    def interact_with_building_1(self):
        print("Player interacted with Building 1: Welcome to the inn!")

    def interact_with_tavern(self):
        print(self.params)
        # self.player = self.params['player']
        self.params['rpg_player'].x  = 620
        self.params['rpg_player'].y  = 634
        g_state_manager.Change(RPGState.TAVERN, self.params)
        
    def interact_with_npc(self, npc):
        # Calculate direction to face player and update NPC sprite
        npc.face_player(self.player.x, self.player.y)
        
        self.current_npc = npc
        self.show_dialogue = True
        self.dialogue_text = npc.dialogue_text or "Hello, traveler! How can I help you?"

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
        if self.params["story_checkpoint"].get("Gate_Open"):
            self.buildings = [b for b in self.buildings if b['id'] != "guard_door"]
        
         # Quest tracking logic
        # Example quest: "Open the gate"
        if not self.params["story_checkpoint"].get("Find_Barkeeper"):
            self.quests["explore"] = "Explore around town for quests"  # Update or add quest
            self.topics["explore"] = "Quests"
        if self.params["story_checkpoint"].get("Gate_Open"):
            self.quests.pop("quest_open_gate", None)  # Remove the quest if gate is open
        elif self.params["story_checkpoint"].get("Find_Barkeeper"):
            self.quests["quest_open_gate"] = "Find a way to open the gate."  # Update or add quest


       
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
                elif event.key == pygame.K_RETURN and self.show_dialogue:
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
        for building in self.buildings:
            pygame.draw.rect(screen, (0, 255, 0), building['rect'], 2)
            
        for npc in self.npcs:
            screen.blit(npc.image, (npc.x, npc.y))  # Render each NPC at its coordinates
                       
        # Render player
        self.player.render(screen)
        
        # Render the quest tracker on top-right
        self.render_quests(screen)
        
        # Render any active dialogue
        self.render_dialogue(screen)
    
    def render_dialogue(self, screen):
        if self.show_dialogue:
            # Render the quest tracker on top-right
            self.render_topics(screen)
            
            # Extend dialogue box to full width
            dialogue_box_x = 50
            dialogue_box_width = SCREEN_WIDTH - 100
            dialogue_box_height = 150
            dialogue_box_y = SCREEN_HEIGHT - 200

            # Render dialogue box
            pygame.draw.rect(screen, (200, 200, 200), (dialogue_box_x, dialogue_box_y, dialogue_box_width, dialogue_box_height))
            font = pygame.font.Font(None, 36)
            
            npc_image = pygame.image.load(self.current_npc.image_path+"/Face.png").convert_alpha()
            npc_image = pygame.transform.scale(npc_image, (400, 400))  # Resize NPC image as needed
            screen.blit(npc_image, (dialogue_box_x + dialogue_box_width - 400, dialogue_box_y - 400))  # Position image above dialogue box
            
            # Render NPC name box above the dialogue box
            name_box_height = 40
            name_box_width = 100
            name_box_y = dialogue_box_y - name_box_height - 10
            pygame.draw.rect(screen, (220, 220, 220), (dialogue_box_x, name_box_y, name_box_width, name_box_height))
            name_font = pygame.font.Font(None, 28)
            npc_name_surface = name_font.render(self.current_npc.name, True, (0, 0, 0))
            # Center the NPC name within the name box
            name_x = dialogue_box_x + (name_box_width - npc_name_surface.get_width()) // 2
            screen.blit(npc_name_surface, (name_x, name_box_y +10))
            
            # Handle multiline dialogue text wrapping
            dialogue_text_lines = self.wrap_text(self.dialogue_text, font, dialogue_box_width - 20)
            line_height = 30
            for i, line in enumerate(dialogue_text_lines):
                dialogue_surface = font.render(line, True, (0, 0, 0))
                screen.blit(dialogue_surface, (dialogue_box_x + 20, dialogue_box_y + 20 + i * line_height))
                
            # Toggle blinking for cursor
            current_time = time.time()
            if current_time - self.last_blink_time > 0.5:  # Blink every 0.5 seconds
                self.blink = not self.blink
                self.last_blink_time = current_time
            
            # Display player input with blinking cursor
            input_text = self.player_input
            if self.blink:
                input_text += "_"  # Add blinking cursor
            player_input_surface = font.render(input_text, True, (0, 0, 255))
            screen.blit(player_input_surface, (70, SCREEN_HEIGHT - 100))

            # Draw "Respond" button
            pygame.draw.rect(screen, (100, 200, 100), self.response_button_rect)
            respond_text = font.render("Respond", True, (255, 255, 255))
            screen.blit(respond_text, (self.response_button_rect.x + 10, self.response_button_rect.y + 10))

            # Draw "Close" button
            pygame.draw.rect(screen, (200, 100, 100), self.close_button_rect)
            close_text = font.render("Close", True, (255, 255, 255))
            screen.blit(close_text, (self.close_button_rect.x + 10, self.close_button_rect.y + 10))
    def render_quests(self, screen):
        
        font = pygame.font.Font(None, 24)
        # Set background dimensions
        background_width = 280
        background_height = 40 + len(self.quests) * 20
        background_x = SCREEN_WIDTH - background_width - 100
        background_y = 10

        # Draw the background with semi-transparency
        background_surface = pygame.Surface((background_width, background_height))
        background_surface.set_alpha(150)  # 150 for semi-transparency
        background_surface.fill((0, 0, 0))  # Black background
        screen.blit(background_surface, (background_x, background_y))

        # Display "Quest" title
        quest_title_surface = font.render("Quest", True, (255, 255, 255))
        screen.blit(quest_title_surface, (background_x + 10, background_y + 10))

        # Display each quest below the title
        for i, quest in enumerate(self.quests):
            quest_text_surface = font.render(self.quests[quest], True, (255, 255, 255))
            screen.blit(quest_text_surface, (background_x + 10, background_y + 40 + i * 20))
    def render_topics(self, screen):
        font = pygame.font.Font(None, 48)
        # Set background dimensions
        topic_background_width = 560
        topic_background_height = 60 + len(self.topics) * 40
        topic_background_x = SCREEN_WIDTH - topic_background_width - 620
        topic_background_y = 10

        # Draw the background with semi-transparency
        topic_background_surface = pygame.Surface((topic_background_width, topic_background_height))
        topic_background_surface.set_alpha(150)  # 150 for semi-transparency
        topic_background_surface.fill((0, 0, 0))  # Black background
        screen.blit(topic_background_surface, (topic_background_x, topic_background_y))

        # Display "Quest" title
        topic_title_surface = font.render("Suggested Conversation Topics", True, (255, 255, 255))
        screen.blit(topic_title_surface, (topic_background_x + 10, topic_background_y + 10))

        # Display each quest below the title
        for i, topic in enumerate(self.topics):
            topic_text_surface = font.render("- "+self.topics[topic], True, (255, 255, 255))
            screen.blit(topic_text_surface, (topic_background_x + 10, topic_background_y + 60 + i * 50))
    def Exit(self):
        pass
