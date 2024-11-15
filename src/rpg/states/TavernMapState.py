# TavernMapState.py
import sys
import time
import pygame
from src.rpg.Resources import ITEM_DESCRIPTIONS
from src.rpg.NPC import NPC
from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT
from src.rpg.EntityDefs import ENTITY_DEFS
from src.rpg.Player import Player
from src.rpg.StateMachine import StateMachine
from src.rpg.Prompts import DEFAULT_TEXT, PROMPTS
from src.resources import g_state_manager
from src.EnumResources import BattleState, RPGState
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
        
        # Menu state
        self.show_menu = False
        self.menu_options = ["Edit Deck", "Inventory", "Exit Game"]
        #Inventory
        self.show_inventory = False
        self.item_options = ["Examine", "Interact"]
        self.selected_item_option = "Examine"
        self.selected_item = 0
        self.showing_options = False
        self.item_interactions = {
            "Health Potion": lambda: print("You drink the Health Potion and restore HP!"),
            "Mana Potion": lambda: print("You drink the Mana Potion and restore MP!")
        }
        

    def toggle_menu(self):
        # Toggle the menu display on/off
        self.show_menu = not self.show_menu
        
    def handle_menu_input(self, event):
        # Navigate the menu options and select one
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE and not self.show_inventory and not self.show_dialogue:
                self.toggle_menu()  # Toggle menu visibility

            elif self.show_menu and not self.show_inventory and not self.show_dialogue:
                if event.key == pygame.K_UP:
                    # Move up in menu options
                    self.selected_option = (self.selected_option - 1) % len(self.menu_options)
                elif event.key == pygame.K_DOWN:
                    # Move down in menu options
                    self.selected_option = (self.selected_option + 1) % len(self.menu_options)
                elif event.key == pygame.K_RETURN:
                    # Execute the selected option
                    self.execute_menu_option()
            
    def execute_menu_option(self):
        # Execute the selected menu option
        if self.menu_options[self.selected_option] == "Edit Deck":
            print("Editing deck...")  # Replace with actual function to edit deck
            g_state_manager.Change(BattleState.DECK_BUILDING, self.params)
        elif self.menu_options[self.selected_option] == "Inventory":
            print("Opening inventory...")  # Replace with actual function to open inventory
            self.show_inventory = True
            self.showing_options = False
        elif self.menu_options[self.selected_option] == "Exit Game":
            pygame.quit()
            sys.exit()
            
    def render_menu(self, screen):
        # Render the escape menu
        if self.show_menu:
            menu_width, menu_height = 300, 200
            menu_x = (screen.get_width() - menu_width) // 2
            menu_y = (screen.get_height() - menu_height) // 2
            pygame.draw.rect(screen, (50, 50, 50), (menu_x, menu_y, menu_width, menu_height))

            font = pygame.font.Font(None, 36)
            for index, option in enumerate(self.menu_options):
                color = (255, 255, 255) if index == self.selected_option else (180, 180, 180)
                option_surface = font.render(option, True, color)
                screen.blit(option_surface, (menu_x + 20, menu_y + 20 + index * 40))
    
    def render_inventory_menu(self,screen, inventory, selected_item, item_options, showing_options, selected_item_option):
        # Inventory Box settings
        inventory_box_x, inventory_box_y = 100, 100
        inventory_box_width, inventory_box_height = 600, 400
        pygame.draw.rect(screen, (240, 240, 240), (inventory_box_x, inventory_box_y, inventory_box_width, inventory_box_height))

        font = pygame.font.Font(None, 32)

        # Display inventory items
        start_y = inventory_box_y + 20
        for i, item in enumerate(inventory):
            item_text = f"{item} x{inventory[item]}"
            item_surface = font.render(item_text, True, (0, 0, 0))
            screen.blit(item_surface, (inventory_box_x + 20, start_y + i * 30))

            # Highlight selected item
            if item == selected_item:
                pygame.draw.rect(screen, (180, 180, 250), (inventory_box_x + 15, start_y + i * 30, inventory_box_width - 30, 30), 2)

        # Show item options for the selected item if activated
        if showing_options:
            option_box_x, option_box_y = inventory_box_x + inventory_box_width - 150, start_y
            pygame.draw.rect(screen, (220, 220, 220), (option_box_x, option_box_y, 120, 100))
            
            # Display options
            for j, option in enumerate(item_options):
                option_text = font.render(option, True, (0, 0, 0))
                screen.blit(option_text, (option_box_x + 10, option_box_y + 10 + j * 30))

                # Highlight selected option
                if option == selected_item_option:
                    pygame.draw.rect(screen, (150, 150, 255), (option_box_x + 5, option_box_y + j * 30, 110, 30), 1)

    def examine_item(self,item):
        """Displays item description."""
        description = ITEM_DESCRIPTIONS.get(item, "No description available.")
        print(f"Examine {item}: {description}")  # This could be replaced with a Pygame popup
        return description
    def next_item_in_inventory(self,inventory, current_item):
        items = list(inventory.keys())
        idx = (items.index(current_item) + 1) % len(items) if current_item else 0
        return items[idx]

    def previous_item_in_inventory(self,inventory, current_item):
        items = list(inventory.keys())
        idx = (items.index(current_item) - 1) % len(items) if current_item else len(items) - 1
        return items[idx]

    def next_option(self,options, current_option):
        idx = (options.index(current_option) + 1) % len(options)
        return options[idx]

    def previous_option(self,options, current_option):
        idx = (options.index(current_option) - 1) % len(options)
        return options[idx]
    
    def add_invisible_wall(self, building_id, x1, y1, x2, y2):
        wall_rect = pygame.Rect(x1, y1, x2 - x1, y2 - y1)
        self.buildings.append({'id': building_id, 'rect': wall_rect, 'interacted': False})
    
    def remove_building_by_id(self, building_id):
        self.buildings = [building for building in self.buildings if building['id'] != building_id]
        
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
            if npc.name == "Thaddeus" and npc.choice == 1:
                self.params['rpg']["story_checkpoint"]["Receive_Parcel"] = True
                self.params['rpg']['Inventory']['Parcel'] = 1
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
            self.handle_menu_input(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.show_dialogue:
                        self.show_dialogue = False
                   
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

            
                # Inventory navigation
                if self.show_inventory and not self.showing_options:
                    self.showing_options = False
                    if event.key == pygame.K_DOWN:
                        self.selected_item = self.next_item_in_inventory(self.params['rpg']['Inventory'], self.selected_item)
                    elif event.key == pygame.K_UP:
                        self.selected_item = self.previous_item_in_inventory(self.params['rpg']['Inventory'], self.selected_item)
                    elif event.key == pygame.K_RETURN and self.selected_item:
                        print("showing option")
                        self.showing_options = True
                    elif event.key == pygame.K_ESCAPE:
                        self.show_inventory = False
                        
                # Option navigation
                elif self.showing_options:
                    if event.key == pygame.K_DOWN:
                        self.selected_item_option = self.next_option(self.item_options, self.selected_item_option)
                    elif event.key == pygame.K_UP:
                        self.selected_item_option = self.previous_option(self.item_options, self.selected_item_option)
                    elif event.key == pygame.K_RETURN:
                        if self.selected_item_option == "Examine":
                            self.examine_item(self.selected_item)
                            self.showing_options = False
                        elif self.selected_item_option == "Interact" and self.selected_item in self.item_interactions:
                            self.item_interactions[self.selected_item]()
                            self.showing_options = False
                    elif event.key == pygame.K_ESCAPE:
                        self.showing_options = False
            
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
        # Render inventory if open
        if self.show_inventory and not self.show_dialogue:
            self.render_inventory_menu(screen, self.params['rpg']['Inventory'], self.selected_item, self.item_options, self.showing_options, self.selected_item_option)
    def Exit(self):
        pass
