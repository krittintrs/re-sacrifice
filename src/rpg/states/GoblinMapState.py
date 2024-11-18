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
from src.battleSystem.battleEntity.Enemy import Enemy as BattleEnemy
from src.battleSystem.battleEntity.entity_defs import BATTLE_ENTITY
from src.rpg.RPGPause import RPGPauseHandler
from src.rpg.Inventory import Inventory

class GoblinMapState:
    def __init__(self):
        scale_factor = 1.5
         # Initialize tavern NPCs
        self.npcs = [
            NPC("Zeus", 281, 430, "src/rpg/sprite/NPC/Zeus_GoblinKing", PROMPTS['Zeus'],'down',scale_factor,DEFAULT_TEXT['Zeus']),
            NPC("Hiw", 449, 136, "src/rpg/sprite/NPC/GoblinGang", PROMPTS['Thaddeus'],'down',0.1,DEFAULT_TEXT['Thaddeus']),
            NPC("Kao", 393, 164, "src/rpg/sprite/NPC/GoblinGang", PROMPTS['Thaddeus'],'down',0.1,DEFAULT_TEXT['Thaddeus']),
            NPC("Timothy", 640, 537, "src/rpg/sprite/NPC/Timothy_GoblinGuard", PROMPTS['Timothy'],'down',1.2,DEFAULT_TEXT['Timothy']),
            NPC("Gruzz", 1125, 236, "src/rpg/sprite/NPC/Steve_GoblinWaterMan", PROMPTS['Gruzz'],'down',1,DEFAULT_TEXT['Gruzz']),
            NPC("Jess", 100, 666, "src/rpg/sprite/NPC/GoblinGang", PROMPTS['Jess'], 'down', 0.1, DEFAULT_TEXT['Jess']),
            NPC("Jude", 493, 469, "src/rpg/sprite/NPC/GoblinGang", PROMPTS['Jude'], 'down', 0.1, DEFAULT_TEXT['Jude']),
        ]
        self.params = None
        self.current_state = self
        # Load the tavern map
        self.map_surface = pygame.image.load("src/rpg/sprite/map/GoblinMap.jpg")
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
        
        self.entering_battle = False
        self.giving_item = False
        
        self.skull_image = pygame.image.load("src/rpg/sprite/Other/skull.png")
        width, height = self.skull_image.get_size()
        reduced_size = (int(width * 0.07), int(height * 0.07))  # Reduce by 10%
        self.skull_image = pygame.transform.smoothscale(self.skull_image, reduced_size)

        self.pauseHandler = RPGPauseHandler(RPGState.GOBLIN)
        self.inventoryHandler = Inventory()        

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
        self.add_invisible_wall("wall_1", 62, 44, 147, 52)        # Wall from (62, 44) to (147, 52)
        self.add_invisible_wall("wall_2", 60, 43, 73, 671)        # Wall from (60, 43) to (73, 671)
        self.add_invisible_wall("wall_3", 245, 56, 1198, 62)      # Wall from (245, 56) to (1198, 62)
        self.add_invisible_wall("wall_4", 1187, 45, 1198, 661)    # Wall from (1187, 45) to (1198, 661)
        self.add_invisible_wall("wall_5", 697, 666, 1198, 680)    # Wall from (697, 666) to (1198, 680)
        self.add_invisible_wall("wall_6", 72, 263, 337, 269)
        self.add_invisible_wall("wall_7", 327, 252, 470, 258)
        self.add_invisible_wall("wall_8", 244, 58, 259, 152)
        self.add_invisible_wall("wall_9", 235, 146, 293, 157)
        self.add_invisible_wall("wall_10", 280, 148, 293, 201)
        self.add_invisible_wall("wall_11", 282, 191, 382, 200)
        self.add_invisible_wall("wall_12", 435, 193, 521, 200)
        self.add_invisible_wall("wall_13", 510, 60, 524, 222)
        self.add_invisible_wall("wall_14", 462, 287, 475, 415)
        self.add_invisible_wall("wall_15", 326, 252, 341, 372)
        self.add_invisible_wall("wall_16", 266, 388, 473, 395)
        self.add_invisible_wall("wall_17", 266, 389, 278, 411)
        self.add_invisible_wall("wall_18", 151, 386, 225, 398)
        self.add_invisible_wall("wall_19", 213, 387, 224, 409)
        self.add_invisible_wall("wall_20", 212, 303, 224, 319)
        self.add_invisible_wall("wall_21", 151, 302, 222, 309)
        self.add_invisible_wall("wall_22", 151, 305, 162, 474)
        self.add_invisible_wall("wall_23", 58, 416, 158, 425)
        self.add_invisible_wall("wall_24", 168, 547, 462, 556)
        self.add_invisible_wall("wall_25", 167, 549, 179, 627)
        self.add_invisible_wall("wall_26", 61, 665, 100, 672)
        self.add_invisible_wall("wall_67", 141, 664, 470, 671)
        self.add_invisible_wall("wall_68", 89, 666, 98, 683)
        self.add_invisible_wall("wall_69", 140, 666, 151, 682)
        self.add_invisible_wall("wall_27", 463, 575, 474, 669)
        self.add_invisible_wall("wall_28", 439, 575, 521, 583)
        self.add_invisible_wall("wall_29", 527, 508, 539, 584)
        self.add_invisible_wall("wall_30", 477, 639, 618, 647)
        self.add_invisible_wall("wall_31", 528, 506, 619, 518)
        self.add_invisible_wall("wall_32", 608, 506, 618, 589)
        self.add_invisible_wall("wall_33", 462, 407, 557, 417)
        self.add_invisible_wall("wall_34", 527, 410, 538, 470)
        self.add_invisible_wall("wall_35", 678, 483, 861, 507)
        self.add_invisible_wall("wall_36", 860, 501, 935, 508)
        self.add_invisible_wall("wall_37", 694, 518, 703, 611)
        self.add_invisible_wall("wall_38", 902, 578, 914, 660)
        self.add_invisible_wall("wall_39", 916, 596, 1009, 603)
        self.add_invisible_wall("wall_40", 917, 599, 932, 661)
        self.add_invisible_wall("wall_41", 924, 483, 936, 510)
        self.add_invisible_wall("wall_42", 923, 484, 1197, 488)
        self.add_invisible_wall("wall_43", 1050, 415, 1063, 487)
        self.add_invisible_wall("wall_44", 1064, 286, 1075, 421)
        self.add_invisible_wall("wall_45", 1064, 287, 1192, 291)
        self.add_invisible_wall("wall_46", 1104, 148, 1193, 157)
        self.add_invisible_wall("wall_47", 1105, 150, 1114, 224)
        self.add_invisible_wall("wall_48", 846, 192, 855, 225)
        self.add_invisible_wall("wall_49", 799, 219, 853, 226)
        self.add_invisible_wall("wall_50", 900, 56, 914, 147)
        self.add_invisible_wall("wall_51", 722, 60, 735, 130)
        self.add_invisible_wall("wall_52", 694, 125, 733, 131)
        self.add_invisible_wall("wall_53", 692, 124, 704, 140)
        self.add_invisible_wall("wall_54", 520, 124, 634, 132)
        self.add_invisible_wall("wall_55", 622, 126, 635, 144)
        self.add_invisible_wall("wall_56", 518, 58, 540, 106)
        self.add_invisible_wall("wall_57", 518, 506, 616, 515)
        self.add_invisible_wall("wall_58", 616, 515, 510, 216)
        self.add_invisible_wall("wall_59", 737, 228, 725, 219)
        self.add_invisible_wall("wall_60", 735, 236, 847, 192)
        self.add_invisible_wall("wall_61", 847, 192, 1027, 201)
        self.add_invisible_wall("wall_62", 511, 217, 736, 229)
        self.add_invisible_wall("wall_63", 726, 220, 736, 236)
        self.add_invisible_wall("wall_64", 849, 416, 970, 423)
        self.add_invisible_wall("wall_65", 1007, 418, 1062, 422)
        self.add_invisible_wall("wall_66", 848, 418, 858, 483)
    
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
        if self.current_npc:
            if self.current_npc.name in ["Jess", "Jude"]:
                if self.current_npc.choice == 1:
                    #self.params['rpg']["exit_battle"] = True
                    #self.params['rpg']['win_battle'] = True # force win
                    self.entering_battle = True
                    pygame.event.get()
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_RETURN]:
                        self.current_npc.choice = 0
                        self.params['rpg']["enter_battle"] = True
                        self.params['rpg']["map"] = "GOBLIN"
                        
                        self.params['battleSystem'] = {
                            'player': self.player.battlePlayer,
                            'enemy': BattleEnemy(BATTLE_ENTITY["default_enemy"])
                        }
                        self.entering_battle = False
                        g_state_manager.Change(BattleState.PREPARATION_PHASE, self.params)

                if self.params['rpg']["exit_battle"]:
                    self.params['rpg']["exit_battle"] = False
                    if self.params['rpg']['win_battle']:
                        self.show_dialogue = False
                        self.current_npc.defeated = True
                    else:
                        if self.current_npc.name == "Jess":
                            self.dialogue_text = self.current_npc.get_dialogue("{Jess remains undefeated! Come back when you're stronger}")
                        else:
                            self.dialogue_text = self.current_npc.get_dialogue("{Jude stands firm! You're not ready to face our king}")

            if self.current_npc.name == "Zeus":
                if self.current_npc.choice == 1 and not self.params['rpg']["enter_battle"]:
                    print("enter battle")
                    self.entering_battle = True
                    pygame.event.get()
                    keys = pygame.key.get_pressed()  # Get current key states
                    if keys[pygame.K_RETURN]:  # Check if Enter key is pressed
                        self.current_npc.choice = 0
                        print("enter battle enter")
                        #TODO Change to goblin king battle
                        self.params['rpg']["enter_battle"] = True
                        self.params['rpg']["map"] = "GOBLIN"
                        self.params['battleSystem'] = {
                            'player': self.player.battlePlayer,
                            'enemy': BattleEnemy(BATTLE_ENTITY["default_enemy"])
                        }
                        self.entering_battle = False
                        g_state_manager.Change(BattleState.PREPARATION_PHASE, self.params)
                if self.params['rpg']["exit_battle"]:
                    self.params['rpg']["exit_battle"] = False
                    if self.params['rpg']['win_battle']:
                        self.current_npc.defeated = True
                    else:
                        self.dialogue_text = self.current_npc.get_dialogue("{You defeated the player}") 
            if self.current_npc.name == "Timothy":
                if self.current_npc.choice == 5 and not self.params['rpg']["enter_battle"]:
                    print("enter battle")
                    self.entering_battle = True
                    pygame.event.get()
                    keys = pygame.key.get_pressed()  # Get current key states
                    if keys[pygame.K_RETURN]:  # Check if Enter key is pressed
                        self.current_npc.choice = 0
                        print("enter battle enter")
                        #TODO Change to goblin king battle
                        self.params['rpg']["enter_battle"] = True
                        self.params['rpg']["map"] = "GOBLIN"
                        self.params['battleSystem'] = {
                            'player': self.player.battlePlayer,
                            'enemy': BattleEnemy(BATTLE_ENTITY["default_enemy"])
                        }
                        self.entering_battle = False
                        g_state_manager.Change(BattleState.PREPARATION_PHASE, self.params)
                if self.params['rpg']["exit_battle"]:
                    self.params['rpg']["exit_battle"] = False
                    if self.params['rpg']['win_battle']:
                        self.current_npc.defeated = True
                        print(f'{self.current_npc.name} is defeated')
                    else:
                        self.dialogue_text = self.current_npc.get_dialogue("{You defeated the player}") 
                if self.current_npc.choice == 1:
                    self.giving_item = True
                    pygame.event.get()
                    keys = pygame.key.get_pressed()  # Get current key states
                    if keys[pygame.K_RETURN]:  # Check if Enter key is pressed
                        self.current_npc.choice = 0
                        if self.params['rpg']['inventory']['Banana'] > 0:
                            self.dialogue_text = self.current_npc.get_dialogue("{the player gave you a real banana, you will let the player pass}") 
                            self.params['rpg']['inventory']['Banana'] += -1
                            self.current_npc.x = 594
                            self.current_npc.y = 592
                        else:
                            self.dialogue_text = self.current_npc.get_dialogue("{the player don't have a banana}") 
                        self.giving_item = False
                            
    def Enter(self, params):
        self.params = params
        print(self.params," Tavern")
        # Transition player position if needed or carry over the current player instance
        self.player = self.params['rpg']['rpg_player']
        print(self.player.x, self.player.y)
        self.show_dialogue = False
        self.dialogue_text = ""
        #print(self.player)
        # self.player.ChangeCoord(x=SCREEN_WIDTH // 2, y=SCREEN_HEIGHT - 100)  # Adjust starting position inside tavern

    def update(self, dt, events):
        if self.inventoryHandler.is_open():
            self.inventoryHandler.update(dt, events, self.params)
            return

        if self.pauseHandler.is_paused():
            inv = self.pauseHandler.update(dt, events, self.params, self.player)
            if inv:
                print(f"Opening {inv}...")  # Replace with actual function to open inventory
                self.inventoryHandler.toggle_inventory()
            else:
                return
        
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.show_dialogue:
                        self.show_dialogue = False
                    else:
                        self.pauseHandler.pause_game()
                elif event.key == pygame.K_RETURN:
                    if self.show_dialogue and not self.entering_battle and not self.giving_item:
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
                            if not npc.defeated:
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
        if (
            not self.show_dialogue 
            and not self.pauseHandler.is_paused() 
            and not self.inventoryHandler.is_open() 
        ):
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
            if not npc.defeated:
                npc_rect = npc.get_rect()
                in_dialogue = self.show_dialogue and self.current_npc == npc
                npc.update(in_dialogue)
                if not npc.defeated:
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
            if npc.defeated:  # If the NPC is defeated, draw the skull image above it
                skull_x = npc.x + (npc.image.get_width() - self.skull_image.get_width()) // 2 +5
                skull_y = npc.y + 10 # Position skull above the NPC
                screen.blit(self.skull_image, (skull_x, skull_y))
    
        self.player.render(screen)
        
        # Render the quest tracker on top-right
        render_quests(screen,self.params['rpg']['quests'])
        
        #render dialogue and topic
        if self.show_dialogue:
            render_topics(screen,self.topics)
            render_dialogue(screen,self.current_npc,self.dialogue_text,self.blink,self.last_blink_time,self.player_input)
            
        self.pauseHandler.render(screen)
        self.inventoryHandler.render(screen, self.params['rpg']['inventory'])
    
    def Exit(self):
        pass
