import pygame
from src.dependency import *
from src.constants import *

class DeckButton:
    def __init__(self, x, y, width, height, text=''):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (150, 150, 150)
        self.clicked_color = (100, 200, 100)
        self.hover_color = (100, 100, 50)
        self.text = text
        self.isClick = False
        self.font = gFont_list["small"]
        self.text_surface = self.font.render(self.text, True, (255, 255, 255))
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

        # resize image
        self.default_image = gDeckButton_image_list["deck_button_default"]
        self.clicked_image = gDeckButton_image_list["deck_button_clicked"]
        self.hover_image = gDeckButton_image_list["deck_button_hover"]
        self.default_image = pygame.transform.scale(self.default_image, (width, height))
        self.clicked_image = pygame.transform.scale(self.clicked_image, (width, height))
        self.hover_image = pygame.transform.scale(self.hover_image, (width, height))
        
    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()

        # draw button
        if self.isClick:
            screen.blit(self.clicked_image, (self.rect.x, self.rect.y))
        else:
            screen.blit(self.default_image, (self.rect.x, self.rect.y))

        # draw text
        screen.blit(self.text_surface, self.text_rect)
        
        # Draw a transparent rectangle if the mouse hovers over the button
        if self.rect.collidepoint(mouse_pos):
            # Create a transparent surface (same size as the button)
            hover_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
            
            # Fill the surface with a color and set the transparency (0-255)
            hover_surface.fill((*self.hover_color, 200))  # Adjust the last value for transparency (100 is semi-transparent)
            
            # Draw the transparent surface onto the screen
            screen.blit(hover_surface, (self.rect.x, self.rect.y))

    def clicked(self, event):
        if self.rect.collidepoint(event.pos):
            self.isClick = not self.isClick
            return True
        else:
            return False