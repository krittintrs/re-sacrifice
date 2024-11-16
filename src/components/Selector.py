import pygame
from src.resources import gSelector_image_list
from src.constants import *

class Selector:
    def __init__(self, name, x=None, y=None, scale=1, center=False):
        self.name = name

        # Load images from the sprite collection
        self.default_image = gSelector_image_list[f"{name}_selector_default"]
        self.clicked_image = gSelector_image_list[f"{name}_selector_clicked"]

        # Resize images
        self.default_image = pygame.transform.scale(
            self.default_image, 
            (int(self.default_image.get_width() * scale), int(self.default_image.get_height() * scale))
        )
        self.clicked_image = pygame.transform.scale(
            self.clicked_image, 
            (int(self.clicked_image.get_width() * scale), int(self.clicked_image.get_height() * scale))
        )

        # Get the dimensions of the button based on the default image
        self.width = self.default_image.get_width()
        self.height = self.default_image.get_height()

        # If the center flag is set, calculate x to center the selector
        if center:
            self.x = (SCREEN_WIDTH - self.width) // 2
        else:
            # Use the provided x value or default to (0, 0)
            self.x = x if x is not None else 0
        
        self.y = y if y is not None else 0

        # Rect for collision detection
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        self.active = False  

    def draw(self, screen):
        """Draws the button on the screen."""
        # Render the image based on whether it is active (selected)
        if self.active:
            screen.blit(self.clicked_image, (self.x, self.y))
        else:
            screen.blit(self.default_image, (self.x, self.y))

    def set_active(self, active):
        """Set the selector as active or inactive."""
        self.active = active
    
    # def draw(self, screen):
    #     """Draws the button on the screen."""
    #     # Get the mouse position
    #     mouse_pos = pygame.mouse.get_pos()

    #     # Check if the mouse is hovering over the button
    #     if self.rect.collidepoint(mouse_pos):
    #         # If hovering, display the clicked image
    #         screen.blit(self.clicked_image, (self.x, self.y))
    #     else:
    #         # Otherwise, display the default image
    #         screen.blit(self.default_image, (self.x, self.y))

    # def is_clicked(self):
    #     """Checks if the button is clicked and returns its name."""
    #     mouse_pos = pygame.mouse.get_pos()
    #     mouse_pressed = pygame.mouse.get_pressed()

    #     # If the mouse is clicked and hovering over the button
    #     if self.rect.collidepoint(mouse_pos) and mouse_pressed[0]:
    #         return self.name  # Return the name of the button
    #     return None
