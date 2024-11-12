import pygame
import sys
from src.rpg.states.TownState import TownState  # Assuming TownState is in src/rpg
from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT
from src.rpg.EntityDefs import ENTITY_DEFS
from src.rpg.StateMachine import StateMachine
from src.rpg.Player import Player
from src.rpg.entity.playerState.PlayerIdleState import PlayerIdleState
from src.rpg.entity.playerState.PlayerWalkState import PlayerWalkState
from src.resources import g_state_manager
import cv2
from src.EnumResources import RPGState

class TutorialState:
    def __init__(self):
        pygame.init()
        #self.screen = pygame.display.get_surface()
        
        player_conf = ENTITY_DEFS['player']
        self.player = Player(player_conf)
        self.player.x = 623
        self.player.y = 585

        self.player.state_machine = StateMachine()
        self.player.state_machine.SetScreen(pygame.display.get_surface())
        self.player.state_machine.SetStates({
            'walk': PlayerWalkState(self.player),
            'idle': PlayerIdleState(self.player)
        })
        self.player.ChangeState('idle')  # Start in idle state
        
        self.params = {'rpg' : {"rpg_player" : self.player,"class": None, "quests":{},"story_checkpoint" : {} ,'Money': None, 'Inventory': {'Health Potion':1,'Mana Potion':1}}, 
                       'card' : {}}
        # Todo: add stater deck params
        
        
         # Load tutorial images or placeholders for instructions and cutscenes
        self.movement_image = pygame.image.load("src/rpg/sprite/Tutorial/images.png")
        self.movement_image = pygame.transform.scale(self.movement_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.battle_image = pygame.image.load("src/rpg/sprite/Tutorial/images (1).png")
        self.battle_image = pygame.transform.scale(self.battle_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.conversation_image = pygame.image.load("src/rpg/sprite/Tutorial/images2.jpg")
        self.conversation_image = pygame.transform.scale(self.conversation_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Track stages within the tutorial
        self.current_stage = "movement"  # Stages: movement, battle, class_select, confirm, cutscene
        self.selected_class = None
        self.confirmation_selection = "confirm"  # Default confirmation selection

        # Classes for selection
        self.classes = ["Mage", "Warrior", "Ranger"]
        self.selected_class_index = 0  # Start with the first class selected
        self.class_img_path = {'Mage': "src/rpg/sprite/Classes/mage.png",
                          'Warrior':"src/rpg/sprite/Classes/warrior.png",
                          'Ranger':"src/rpg/sprite/Classes/ranger.png"}
        self.class_desc = {'Mage': "Magic go boom",
                          'Warrior':"ching ching",
                          'Ranger':"Pung Pung"}
        # Confirmation buttons
        self.confirm_rect = pygame.Rect(650, 500, 100, 40)
        self.cancel_rect = pygame.Rect(760, 500, 100, 40)
        
        # Initialize font
        self.font = pygame.font.Font(None, 36)
        self.title_font = pygame.font.Font(None, 48)  # Font for the title
        
        # Video setup for cutscene
        self.cutscene_video = cv2.VideoCapture("src/rpg/cutscene/Cutscene1.mp4")
        self.playing_cutscene = False
        
    def update(self, dt,events):
         for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if self.current_stage == "cutscene" and self.playing_cutscene:
                        self.skip_cutscene()
                    else:
                        self.handle_enter()
                elif self.current_stage == "class_select":
                    if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                        self.selected_class_index = (self.selected_class_index - 1) % len(self.classes)
                    elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                        self.selected_class_index = (self.selected_class_index + 1) % len(self.classes)
                elif self.current_stage == "confirm":
                    if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                        self.confirmation_selection = "confirm"
                    elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                        self.confirmation_selection = "cancel"
                        
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.confirm_rect.collidepoint(mouse_pos):
                    self.handle_confirm_selection()
                elif self.cancel_rect.collidepoint(mouse_pos):
                    self.current_stage = "class_select"  # Go back to class selection

    def Enter(self, enter_params):
        if enter_params:
            self.params = enter_params
        print(self.params," Tutorial")
        
        print("Entering Tutorial State")
        
    def handle_enter(self):
        if self.current_stage == "movement":
            self.current_stage = "conversation"
        elif self.current_stage == "conversation":
            self.current_stage = "battle"
        elif self.current_stage == "battle":
            self.current_stage = "class_select"
        elif self.current_stage == "class_select":
            self.selected_class = self.classes[self.selected_class_index]
            self.current_stage = "confirm"
        elif self.current_stage == "confirm":
            if self.confirmation_selection == "confirm":
                self.current_stage = "cutscene"
                self.playing_cutscene = True  # Start cutscene playback
            else:
                self.current_stage = "class_select"
        elif self.current_stage == "cutscene":
            g_state_manager.Change(RPGState.TOWN, self.params)  # Transition to RPG start state

    def skip_cutscene(self):
        self.playing_cutscene = False
        self.cutscene_video.release()  # Release video resource
        g_state_manager.Change(RPGState.TOWN, self.params)
        
    def render_cutscene(self, screen):
        ret, frame = self.cutscene_video.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = pygame.surfarray.make_surface(frame)
            frame = pygame.transform.scale(frame, (SCREEN_WIDTH, SCREEN_HEIGHT))
            screen.blit(frame, (0, 0))
        else:
            self.skip_cutscene()  # End cutscene when the video is finished
            
    def handle_confirm_selection(self):
        if self.confirmation_selection == "confirm":
            self.current_stage = "cutscene"
        else:
            self.current_stage = "class_select"  # Go back to class selection

    def move_selection(self, direction):
        if self.phase == 3:
            self.selected_index = (self.selected_index + direction) % len(self.classes)
    
    def render(self, screen):
        if self.current_stage == "movement":
            screen.blit(self.movement_image, (0, 0))
            self.render_text(screen, "Use WASD to move and Space to interact. Press Enter to continue.", (50, SCREEN_HEIGHT - 50))
        
        elif self.current_stage == "conversation":
            screen.blit(self.conversation_image, (0, 0))
            self.render_text(screen, "Here's how to have conversation. Press Enter to continue.", (50, SCREEN_HEIGHT - 50))
        
        elif self.current_stage == "battle":
            screen.blit(self.battle_image, (0, 0))
            self.render_text(screen, "Here's how to battle. Press Enter to continue.", (50, SCREEN_HEIGHT - 50))
        
        elif self.current_stage == "class_select":
            self.render_class_selection(screen)
        
        elif self.current_stage == "confirm":
            self.render_confirmation(screen)
        
        elif self.current_stage == "cutscene":
            if self.playing_cutscene:
                self.render_cutscene(screen)

    def render_class_selection(self, screen):
        screen.fill((30, 30, 30))
        num_classes = len(self.classes)
        section_width = SCREEN_WIDTH // num_classes
        image_size = (section_width * 0.6, section_width * 0.6)
        
        # Draw title at the top
        title_text = self.title_font.render("Choose Your Class", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
        screen.blit(title_text, title_rect)

        for i, cls in enumerate(self.classes):
            # Calculate position and area for each class section
            x = i * section_width
            y = 150  # Y position offset below the title
            # Load and scale image
            image = pygame.image.load(self.class_img_path[cls])
            image = pygame.transform.scale(image, image_size)
            image_rect = image.get_rect(center=(x + section_width // 2, y + image_size[1] // 2))
            screen.blit(image, image_rect)

            # Draw class name below the image
            name_text = self.font.render(cls, True, (255, 255, 255))
            name_rect = name_text.get_rect(center=(x + section_width // 2, y + image_size[1] + 40))
            screen.blit(name_text, name_rect)

            # Draw class description below the name
            description = self.font.render(self.class_desc[cls], True, (200, 200, 200))
            description_rect = description.get_rect(center=(x + section_width // 2, y + image_size[1] + 80))
            screen.blit(description, description_rect)

            # Draw border if this is the selected class
            if i == self.selected_class_index:
                pygame.draw.rect(screen, (255, 215, 0), (x, y, section_width, image_size[1] + 100), 5)


    def render_confirmation(self, screen):
        screen.fill((30, 30, 30))
        self.render_text(screen, f"Are you sure you want to be a {self.selected_class}?", (50, 50))
        
        # Draw Confirm and Cancel buttons with a border around the selected one
        pygame.draw.rect(screen, (0, 255, 0) if self.confirmation_selection == "confirm" else (255, 255, 255), self.confirm_rect, 3)
        pygame.draw.rect(screen, (0, 255, 0) if self.confirmation_selection == "cancel" else (255, 255, 255), self.cancel_rect, 3)
        
        confirm_text = self.font.render("Confirm", True, (255, 255, 255))
        cancel_text = self.font.render("Cancel", True, (255, 255, 255))
        
        screen.blit(confirm_text, (self.confirm_rect.x + 10, self.confirm_rect.y + 5))
        screen.blit(cancel_text, (self.cancel_rect.x + 10, self.cancel_rect.y + 5))

    def render_text(self, screen, text, position):
        font = pygame.font.Font(None, 36)
        text_surface = font.render(text, True, (255, 255, 255))
        screen.blit(text_surface, position)

    def Exit(self):
        if self.playing_cutscene:
            self.cutscene_video.release()