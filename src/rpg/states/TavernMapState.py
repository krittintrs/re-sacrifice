# TavernMapState.py
import sys
import time
import pygame
from src.rpg.NPC import NPC
from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT
from src.rpg.EntityDefs import ENTITY_DEFS
from src.rpg.Player import Player
from src.rpg.StateMachine import StateMachine
from src.rpg.Prompts import DEFAULT_TEXT, PROMPTS
from src.resources import g_state_manager
from src.EnumResources import RPGState
from src.rpg.Utils import render_dialogue, render_interaction_dialogue,render_quests,render_topics

class TavernMapState:
    def __init__(self):
        scale_factor = 2
         # Initialize tavern NPCs
        self.npcs = [
            NPC("John", 650, 375, "src/rpg/sprite/NPC/John_Tavernkeeper", PROMPTS['John'], 'left',scale_factor,"Hello, traveler! How can I help you?"),
            NPC("Thaddeus", 994, 410, "src/rpg/sprite/NPC/Thaddeus_OldMan", PROMPTS['Thaddeus'],'down',scale_factor,DEFAULT_TEXT['Thaddeus'])
        ]
        self.params = None
        self.current_state = self
        # Load the tavern map
        self.map_surface = pygame.image.load("src/rpg/sprite/map/TavernMap.jpg")
        self.map_surface = pygame.transform.scale(self.map_surface, (SCREEN_WIDTH, SCREEN_HEIGHT))
    
        # Dialogue state
        self.show_dialogue = False
        self.dialogue_text = ""
        self.player_input = ""
        self.response_button_rect = pygame.Rect(650, 500, 100, 40)
        self.close_button_rect = pygame.Rect(760, 500, 100, 40)
        self.current_npc = None
        self.selected_option = 0

        self.last_blink_time = 0
        self.blink = False
        
        # Initialize buildings and interactions
        self.buildings = []
        self.building_interactions = {
            "door": self.interact_with_door,
            "bar": self.interact_with_bar,
            "wall": self.interact_none
            # "tavern_building": self.interact_with_tavern,
            # # "John_npc": lambda: self.interact_with_npc("John", "Hello, traveler! I am John, the town's guide.")
        }
        self.generate_buildings()  # Add buildings with invisible walls
        
        
        # State variables
        self.show_dialogue = False
        self.dialogue_text = ""
        self.current_npc = None
        self.topics = {}
        

        
    def scale_entities(self, scale_factor):
        # Scale player and NPC dimensions and position
        for entity in [self.npcs]:
            entity = entity[0]
            print(entity)
            entity.update_sprite(scale_factor)
                   
    def add_invisible_wall(self, building_id, x1, y1, x2, y2):
        wall_rect = pygame.Rect(x1, y1, x2 - x1, y2 - y1)
        self.buildings.append({'id': building_id, 'rect': wall_rect, 'interacted': False})
    
    def generate_buildings(self):
        #Walls
        self.add_invisible_wall("wall", 523, 552, 536, 703)
        self.add_invisible_wall("wall", 727, 551, 743, 702)
        self.add_invisible_wall("wall", 743, 582, 1219, 618)
        self.add_invisible_wall("wall", 46, 584, 521, 599)
        self.add_invisible_wall("wall", 40, 146, 147, 579)
        self.add_invisible_wall("wall", 140, 138, 294, 262)
        self.add_invisible_wall("wall", 1180, 24, 1229, 580)
        self.add_invisible_wall("wall", 992, 318, 1181, 357)
        self.add_invisible_wall("wall", 1128, 349, 1177, 402)
        self.add_invisible_wall("bar", 534, 445, 814, 482)
        self.add_invisible_wall("bar", 730, 370, 819, 482)
        self.add_invisible_wall("bar", 532, 373, 609, 476)
        self.add_invisible_wall("wall", 298, 308, 356, 442)
        self.add_invisible_wall("wall", 358, 393, 492, 442)
        self.add_invisible_wall("wall", 140, 138, 294, 262)
        self.add_invisible_wall("wall", 219, 4, 260, 136)
        self.add_invisible_wall("wall", 927, 26, 1227, 54)
        self.add_invisible_wall("wall", 263, 3, 1177, 110)
        self.add_invisible_wall("wall", 140, 138, 294, 262)
        self.add_invisible_wall("wall", 140, 138, 294, 262)
        # #NPC
        # self.add_invisible_wall("John_npc", 411, 453, 440, 480)
        # Add a door interaction
        self.add_invisible_wall("door", 538, 694, 730, 718)  # Adjust coordinates for the door
    def interact_none(self):
        print("interacted")
    def interact_with_door(self):
        # Transition back to the TownState
        self.params['rpg']["rpg_player"].x = 625
        self.params['rpg']["rpg_player"].y = 326
        g_state_manager.Change(RPGState.TOWN, self.params)
        
    def interact_with_bar(self):
        # Transition back to the TownState
        self.interact_with_npc(self.npcs[0])

    def interact_with_npc(self, npc):
        # Calculate direction to face player and update NPC sprite
        npc.face_player(self.player.x, self.player.y)
        
        
        self.current_npc = npc
        self.show_dialogue = True
        self.dialogue_text = npc.dialogue_text or npc.default_text
    
    def update_story(self):
        for npc in self.npcs:
            if npc.name == "John" and npc.choice == 1:
                self.params['rpg']["story_checkpoint"]["Gate_Open"] = True
    def Enter(self, params):
        self.params = params
        print(self.params," Tavern")
        # Transition player position if needed or carry over the current player instance
        self.player = self.params['rpg']['rpg_player']
        print(self.player.x, self.player.y)
        self.show_dialogue = False
        self.dialogue_text = ""
        self.current_npc = None
        #print(self.player)
        # self.player.ChangeCoord(x=SCREEN_WIDTH // 2, y=SCREEN_HEIGHT - 100)  # Adjust starting position inside tavern

    def update(self, dt, events):
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
                        self.player_input = "ok"  # Default to "ok" if input is empty
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
                                print(self.player.x,self.player.y)
                                print(f"interact with npc {npc.name}")
                                self.interact_with_npc(npc)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.show_dialogue:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.close_button_rect.collidepoint(mouse_pos):
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
        self.update_story()
        self.player.update(dt, events)

    def render(self, screen):
        # Draw map
        screen.blit(self.map_surface, (0, 0))

        # Draw invisible walls as green rectangles for debugging
        for building in self.buildings:
            pygame.draw.rect(screen, (0, 255, 0), building['rect'], 2)
            
        for npc in self.npcs:
            screen.blit(npc.image, (npc.x, npc.y))  # Render each NPC at its coordinates
    
        self.player.render(screen)
        
        # Render the quest tracker on top-right
        render_quests(screen,self.params['rpg']['quests'])
        #render dialogue and topic
        if self.show_dialogue:
            render_topics(screen,self.topics)
            render_dialogue(screen,self.current_npc,self.dialogue_text,self.blink,self.last_blink_time,self.player_input)
    
    def Exit(self):
        pass
