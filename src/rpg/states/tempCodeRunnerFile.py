import sys
import pygame
from src.rpg.entity.playerState.PlayerIdleState import PlayerIdleState
from src.rpg.entity.playerState.PlayerWalkState import PlayerWalkState
from src.rpg.EntityDefs import ENTITY_DEFS
from src.rpg.Player import Player
from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT
from src.rpg.StateMachine import StateMachine

class TownState:
    def __init__(self):
        # Load the full-scale map without resizing
        self.map_surface = pygame.image.load("src/rpg/sprite/map/TownMap.jpg")
        self.map_width, self.map_height = self.map_surface.get_size()
        print(self.map_width,self.map_height)

        # Camera offset (initially zeroed to start from the top-left of the map)
        self.camera_x = 0
        self.camera_y = 0

    def Enter(self, enter_params):
        # Initialize player configuration
        player_conf = ENTITY_DEFS['player']
        self.player = Player(player_conf)
        self.player.state_machine = StateMachine()
        self.player.state_machine.SetScreen(pygame.display.get_surface())
        self.player.state_machine.SetStates({
            'walk': PlayerWalkState(self.player),
            'idle': PlayerIdleState(self.player)
        })
        self.player.ChangeState('idle')  # Start in idle state
        print("Entering RPG Start State")

    def Exit(self):
        print("Exiting RPG Start State")
        
    def update(self, dt, events):
    # Handle events
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        # Handle player movement based on keyboard input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.player.MoveY(-self.player.walk_speed * dt)
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.player.MoveY(self.player.walk_speed * dt)
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.player.MoveX(-self.player.walk_speed * dt)
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.player.MoveX(self.player.walk_speed * dt)

        # Clamp player within map boundaries
        self.player.x = max(0, min(self.map_width - self.player.width, self.player.x))
        self.player.y = max(0, min(self.map_height - self.player.height, self.player.y))

        # Lock the camera on the player, ensuring it doesn't exceed map boundaries
        self.camera_x = max(0, min(self.player.x - SCREEN_WIDTH // 2, self.map_width - SCREEN_WIDTH))
        self.camera_y = max(0, min(self.player.y - SCREEN_HEIGHT // 2, self.map_height - SCREEN_HEIGHT))

        # Update player state and animations
        self.player.update(dt, events)


    def render(self, screen):
        # Draw the visible part of the map based on the camera position
        screen.blit(self.map_surface, (0, 0), (self.camera_x, self.camera_y, SCREEN_WIDTH, SCREEN_HEIGHT))

        # Offset player render position by camera position
        player_render_x = self.player.x - self.camera_x
        player_render_y = self.player.y - self.camera_y
        self.player.render(screen, player_render_x, player_render_y)
