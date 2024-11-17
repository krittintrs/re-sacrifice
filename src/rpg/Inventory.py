import sys
import pygame
from src.rpg.Resources import ITEM_DESCRIPTIONS
from src.rpg.Utils import render_interaction_dialogue

class Inventory:
    def __init__(self):
        #Inventory
        
        self.item_options = ["Examine", "Interact"]
        self.selected_item_option = "Examine"
        self.selected_item = 0

        self.show_inventory = False
        self.showing_options = False
        self.show_popup = False

        self.item_interactions = {
            "Health Potion": lambda: print("You drink the Health Potion and restore HP!"),
            "Mana Potion": lambda: print("You drink the Mana Potion and restore MP!")
        }
    
    def is_open(self):
        return self.show_inventory
    
    def toggle_inventory(self):
        self.show_inventory = not self.show_inventory
        self.selected_item = 0
        self.showing_options = False

    def examine_item(self, item):
        """Displays item description."""
        description = ITEM_DESCRIPTIONS.get(item, "No description available.")
        print(f"Examine {item}: {description}")  # This could be replaced with a Pygame popup
        self.show_popup = True
        self.popup = "Item_Description"
        self.popup_text = description  # Store the dialogue text for rendering in the popup
    
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
    
    def update(self, dt, events, params):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                # Inventory navigation
                if self.show_inventory and not self.showing_options and not self.show_popup:
                    self.showing_options = False
                    if event.key == pygame.K_DOWN:
                        self.selected_item = self.next_item_in_inventory(params['rpg']['inventory'], self.selected_item)
                    elif event.key == pygame.K_UP:
                        self.selected_item = self.previous_item_in_inventory(params['rpg']['inventory'], self.selected_item)
                    elif event.key == pygame.K_RETURN and self.selected_item:
                        print("showing option")
                        self.showing_options = True
                    elif event.key == pygame.K_ESCAPE:
                        self.show_inventory = False
                        
                # Option navigation
                elif self.showing_options and not self.show_popup:
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

                # Close examination popup
                elif self.show_popup:
                    if event.key == pygame.K_RETURN:
                        self.show_popup = False
                    if event.key == pygame.K_ESCAPE:
                        self.show_popup = False

    def render(self, screen, inventory):
        # Render inventory if open
        if self.show_inventory:
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
                if item == self.selected_item:
                    pygame.draw.rect(screen, (180, 180, 250), (inventory_box_x + 15, start_y + i * 30, inventory_box_width - 30, 30), 2)

            # Show item options for the selected item if activated
            if self.showing_options:
                option_box_x, option_box_y = inventory_box_x + inventory_box_width - 150, start_y
                pygame.draw.rect(screen, (220, 220, 220), (option_box_x, option_box_y, 120, 100))
                
                # Display options
                for j, option in enumerate(self.item_options):
                    option_text = font.render(option, True, (0, 0, 0))
                    screen.blit(option_text, (option_box_x + 10, option_box_y + 10 + j * 30))

                    # Highlight selected option
                    if option == self.selected_item_option:
                        pygame.draw.rect(screen, (150, 150, 255), (option_box_x + 5, option_box_y + j * 30, 110, 30), 1)
        
            if self.show_popup:
                render_interaction_dialogue(screen, self.popup_text, enter_action_text="Enter", escape_action_text="Escape")
                    