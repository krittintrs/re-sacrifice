import sys
import time
import pygame
from src.rpg.entity.playerState.PlayerIdleState import PlayerIdleState
from src.rpg.entity.playerState.PlayerWalkState import PlayerWalkState
from src.rpg.EntityDefs import ENTITY_DEFS
from src.rpg.Player import Player
from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT
from src.rpg.StateMachine import StateMachine
from src.rpg.NPC import NPC
from src.rpg.Prompts import *
from src.resources import g_state_manager
from src.EnumResources import BattleState, RPGState
from src.rpg.Utils import render_dialogue, render_interaction_dialogue,render_quests,render_topics
from src.rpg.Resources import ITEM_DESCRIPTIONS

# genai.configure(api_key="AIzaSyAbw1QNIQlmYgTYdsgLiOELef10E-M6BJY")genai.configure(api_key="AIzaSyAbw1QNIQlmYgTYdsgLiOELef10E-M6BJY")
# Create the model


class TownState:
    def __init__(self):
        pygame.init()
        
        self.scale_factor = 1.5
        
        # Initialize map
        self.map_surface = pygame.image.load("src/rpg/sprite/map/TownMap.jpg")
        self.map_surface = pygame.transform.scale(self.map_surface, (SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Initialize NPCs with unique prompts
        self.npcs = [
            NPC("Jim", 411, 453, "src/rpg/sprite/NPC/Jim_GoblinHunter", PROMPTS['Jim'],'right',self.scale_factor,DEFAULT_TEXT['Jim']),
            NPC("Susan", 811, 453, "src/rpg/sprite/NPC/Susan_Trivia", PROMPTS['Susan'],'down',self.scale_factor,DEFAULT_TEXT['Susan']),
            NPC("Mira", 1103, 329, "src/rpg/sprite/NPC/Mira_Weaver", PROMPTS['Mira'],'left',self.scale_factor,DEFAULT_TEXT['Mira']),
            NPC("Jarek", 235, 291, "src/rpg/sprite/NPC/Jarek_Repairman", PROMPTS['Jarek'],'up',self.scale_factor,DEFAULT_TEXT['Jarek']),
            NPC("Guard", 627, 51, "src/rpg/sprite/NPC/Guard_Guard", PROMPTS['Guard'],'down',self.scale_factor,DEFAULT_TEXT['Guard']),
            NPC("Elara", 142, 574, "src/rpg/sprite/NPC/Elara_StrongWoman", PROMPTS['Elara'],'down',self.scale_factor,DEFAULT_TEXT['Elara'])
            # Add more NPCs here
        ]

        # Dialogue state
        self.show_dialogue = False
        self.dialogue_text = ""
        self.player_input = ""
        self.show_popup = False
        self.popup = None
        self.popup_text = ""
        
        self.current_npc = None
        self.selected_option = 0
        self.closing_dialogue = False

        self.last_blink_time = 0
        self.blink = False
        
        # Menu state
        self.show_menu = False
        self.menu_options = ["Edit Deck", "Inventory", "Exit Game"]
        self.selected_option = 0
        #Inventory
        self.show_inventory = False
        self.item_options = ["Examine", "Interact"]
        self.selected_item = 0
        self.showing_options = False
        self.item_interactions = {
            "Health Potion": lambda: print("You drink the Health Potion and restore HP!"),
            "Mana Potion": lambda: print("You drink the Mana Potion and restore MP!")
        }
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
                
        self.params = None 
        # Initialize this attribute in the __init__ method or class constructor
        self.gate_open = False
        
        # Initialize buildings and interactions
        self.buildings = []
        self.building_interactions = {
            "blacksmith_building": self.interact_with_building_1,
            "tavern_building": self.interact_with_tavern,
            "goblin_entrance": self.interact_with_goblin_entrance,
            "blacksmith_building": self.interact_with_blacksmith
            # "John_npc": lambda: self.interact_with_npc("John", "Hello, traveler! I am John, the town's guide.")
        }
        self.generate_buildings()  # Add buildings with invisible walls
        self.topics = {}
    def Enter(self, enter_params):
        self.params = enter_params
        self.player = enter_params['rpg']['rpg_player']
        print(self.params," TownMap")
        
        print("Entering RPG Start State")
    
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
            elif event.key == pygame.K_ESCAPE and self.show_inventory:
                self.show_inventory = not self.show_inventory
    def execute_menu_option(self):
        # Execute the selected menu option
        if self.menu_options[self.selected_option] == "Edit Deck":
            print("Editing deck...")  # Replace with actual function to edit deck
            g_state_manager.Change(BattleState.DECK_BUILDING, self.params)
        elif self.menu_options[self.selected_option] == "Inventory":
            print("Opening inventory...")  # Replace with actual function to open inventory
            self.show_inventory = not self.show_inventory
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
    
    def render_inventory_menu(self,screen, inventory, selected_item, item_options, showing_options, selected_option):
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
            print("showing option")
            option_box_x, option_box_y = inventory_box_x + inventory_box_width - 150, start_y
            pygame.draw.rect(screen, (220, 220, 220), (option_box_x, option_box_y, 120, 100))
            
            # Display options
            for j, option in enumerate(item_options):
                option_text = font.render(option, True, (0, 0, 0))
                screen.blit(option_text, (option_box_x + 10, option_box_y + 10 + j * 30))

                # Highlight selected option
                if option == selected_option:
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
    
    def generate_buildings(self):
        #Buildings
        self.add_invisible_wall("blacksmith_building", 177, 130, 437, 258)
        self.add_invisible_wall("tavern_wall", 510, 120, 760, 295)
        self.add_invisible_wall("tavern_building", 617, 258, 662, 298)
        self.add_invisible_wall("market1_building", 922, 90, 1106, 246)
        self.add_invisible_wall("market2_building", 867, 262, 1047, 368)
        self.add_invisible_wall("residence_building", 846, 442, 1115, 558)
        self.add_invisible_wall("store_wall", 509, 437, 766, 590)
        self.add_invisible_wall("store_building", 614, 579, 664, 592)
        self.add_invisible_wall("goblin_entrance", 596, 1, 675, 10)
        self.add_invisible_wall("goblin_entrance2", 279, 2, 356, 10)
        #Walls
        self.add_invisible_wall("south_wall", 48, 640, 1227, 676)
        self.add_invisible_wall("west_wall", 37, 51, 91, 629)
        self.add_invisible_wall("north_wall1", 94, 55, 598, 72)
        self.add_invisible_wall("north_wall2", 676, 34, 1239, 72)
        self.add_invisible_wall("north_wall3", 261, 5, 277, 53)
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
        self.params['rpg']['rpg_player'].x  = 620
        self.params['rpg']['rpg_player'].y  = 634
        g_state_manager.Change(RPGState.TAVERN, self.params)
        
    def interact_with_goblin_entrance(self):
        dialogue_text = (
            "Do you want to continue to the Goblin Camp? "
            "After entering, you won’t be able to come back to the town unless the Goblin King is defeated. "
            "Prepare everything carefully. Press Enter to enter or else press Escape."
        )
        
        # Trigger the popup with specific settings for the goblin camp entrance
        self.show_popup = True
        self.popup = "Goblin_Entrance"
        self.popup_text = dialogue_text  # Store the dialogue text for rendering in the popup
    
    def interact_with_blacksmith(self):
        dialogue_text = (
            "A broken blacksmith building"
        )
        
        # Trigger the popup with specific settings for the goblin camp entrance
        self.show_popup = True
        self.popup = "Goblin_Entrance"
        self.popup_text = dialogue_text  # Store the dialogue text for rendering in the popup
      
    def interact_with_npc(self, npc):
        # Calculate direction to face player and update NPC sprite
        npc.face_player(self.player.x, self.player.y)
        
        self.current_npc = npc
        self.show_dialogue = True
        self.dialogue_text = npc.dialogue_text or npc.default_text

    def update_topics(self):
        self.topics = {}
        if not self.params['rpg']["story_checkpoint"].get("Find_Barkeeper"):
            self.topics["Find_Quests"] = "Finding Quests"
            
        if self.current_npc:
            #Mira Jarek quest
            if self.current_npc.name == "Jim":
                None

    def update_story(self):
        #Main Goblin Quest
        if not self.params['rpg']["story_checkpoint"].get("Find_Barkeeper"):
            self.params['rpg']['quests']["Goblin"] = "Explore around town for quests"  # Update or add quest
        for npc in self.npcs:
            if npc.choice == 5:
                self.params['rpg']["story_checkpoint"]["Find_Barkeeper"] = True
                self.params['rpg']['quests']["Goblin"] = "Find the Barkeeper" 
        if self.params['rpg']["story_checkpoint"].get("Gate_Open"):
            if not self.gate_open:  # Check if the message has already been shown
                print("Gate open!")  # Print the message
                for npc in self.npcs:
                    if npc.name == "Guard":
                        npc.x = 597
                        npc.y = 76
                        npc.get_dialogue("{the player got a quest that allow them to go to the goblin cave. Also don't forget to warn the player that if they decide to leave town they cannot come back to the town unless the goblin king is dead for safety reasons.}")
                self.gate_open = True  # Set flag to True so it doesn't print again
            self.params['rpg']['quests']["Goblin"] = "Go to the goblin camp"
        if self.params['rpg']["story_checkpoint"].get("Gate_Open"):
            self.buildings = [b for b in self.buildings if b['id'] != "guard_door"]
        
        if self.current_npc:
            
            #Mira Jarek quest
            if self.current_npc.name == "Mira":
                if self.current_npc.choice == 0:
                    ['rpg']['quests']["Mira_Jarek"] = "Fix Mira's relationship" 
            elif self.current_npc.name == "Jarek":
                if self.current_npc.choice == 3:
                    self.current_npc.get_dialogue("{You break up with Mira and now hate her}") 
                if self.current_npc.choice == 1 and not self.params['rpg']["story_checkpoint"].get("Help_Mira"):
                    self.closing_dialogue = True
                    pygame.event.get()
                    keys = pygame.key.get_pressed()  # Get current key states
                    if keys[pygame.K_RETURN]:  # Check if Enter key is pressed
                        self.show_dialogue = False  # Close the dialogue box
                        self.params['rpg']["story_checkpoint"]["Help_Mira"] = True
                        self.current_npc.x = 1069
                        self.current_npc.y = 329
                        self.params['rpg']["Inventory"]["Banana"] = 1
                        self.current_npc.get_dialogue("{You have returned to Mira and you are now standing next to Mira at her shop}")
                        self.current_npc = None
                        for npc in self.npcs:
                            if npc.name == "Mira":
                                npc.get_dialogue("{Jarek have returned to you and you are now standing next to Jarek at your shop because the player convinced Jarek to return to you}")
                        self.params['rpg']['quests'].pop("Mira_Jarek",None)
                        self.closing_dialogue = False
        
    def update(self, dt, events):
        # Handle events
        for event in events:
            self.handle_menu_input(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.show_dialogue:
                        self.show_dialogue = False
                    elif self.show_popup:  # Close the goblin camp popup if it's active
                        self.show_popup = False
                    # else:
                    #     pygame.quit()
                    #     sys.exit()
                elif event.key == pygame.K_RETURN:
                    if self.show_popup:
                        if self.popup == "Goblin_Entrance":
                            self.show_popup = False
                            print("Enter Goblin Camp")
                    elif self.show_dialogue and not self.closing_dialogue:
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
                                print(f"interact with npc {npc.name}")
                                self.interact_with_npc(npc)
                # Inventory navigation
                if self.show_inventory and not self.show_dialogue:
                    if event.key == pygame.K_DOWN:
                        self.selected_item = self.next_item_in_inventory(self.params['rpg']['Inventory'], self.selected_item)
                    elif event.key == pygame.K_UP:
                        self.selected_item = self.previous_item_in_inventory(self.params['rpg']['Inventory'], self.selected_item)
                    elif event.key == pygame.K_RETURN and self.selected_item:
                        self.showing_options = True  # Show options for the selected item

                    # Option navigation
                    if self.showing_options:
                        if event.key == pygame.K_DOWN:
                            selected_option = self.next_option(self.item_options, selected_option)
                        elif event.key == pygame.K_UP:
                            selected_option = self.previous_option(self.item_options, selected_option)
                        elif event.key == pygame.K_RETURN:
                            # Execute action based on option
                            if self.selected_option == "Examine":
                                description = self.examine_item(self.selected_item)
                                print(description)  # Show a popup or text for item description
                            elif self.selected_option == "Interact" and self.selected_item in self.item_interactions:
                                self.item_interactions[self.selected_item]()  # Execute unique interaction
                            self.showing_options = False
                        elif event.key == pygame.K_ESCAPE:
                            self.showing_options = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                print(f"Mouse clicked at: ({mouse_x}, {mouse_y})")

        # Store original player position to revert if collision occurs
        original_x, original_y = self.player.x, self.player.y

        # Handle player movement
        keys = pygame.key.get_pressed()
        if not self.show_dialogue and not self.show_popup and not self.show_menu and not self.show_inventory:
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
        self.update_topics()

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
        render_quests(screen,self.params['rpg']['quests'])
        
        #render dialogue and topic
        if self.show_dialogue :
            render_topics(screen,self.topics)
            render_dialogue(screen,self.current_npc,self.dialogue_text,self.blink,self.last_blink_time,self.player_input)
            
        #render popup
        if self.show_popup:
            if self.popup == "Goblin_Entrance":
                render_interaction_dialogue(screen, self.popup_text, enter_action_text="Enter", escape_action_text="Escape")
                
        # Render the escape menu if it's active
        if self.show_menu and not self.show_dialogue:
            self.render_menu(screen)
            
        # Render inventory if open
        if self.show_inventory and not self.show_dialogue:
            self.render_inventory_menu(screen, self.params['rpg']['Inventory'], self.selected_item, self.item_options, self.showing_options, self.selected_option)
    def Exit(self):
        pass
