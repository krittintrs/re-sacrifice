import os
import random
import pygame
import google.generativeai as genai
import re
import json

# Create the model
generation_config = {
  "temperature": 1.5,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}
class NPC:
    def __init__(self, name, x, y, image_path, prompt, default_dir,scale_factor):
        self.name = name
        self.x = x
        self.y = y
        # scale_factor = 1.5  # Scale factor for increasing size
        self.image_path = image_path
        # Load and scale directional sprites
        self.sprites = {
            'up': pygame.transform.scale(pygame.image.load(os.path.join(image_path, 'up.png')),
                                         (int(pygame.image.load(os.path.join(image_path, 'up.png')).get_width() * scale_factor),
                                          int(pygame.image.load(os.path.join(image_path, 'up.png')).get_height() * scale_factor))),
            'down': pygame.transform.scale(pygame.image.load(os.path.join(image_path, 'down.png')),
                                           (int(pygame.image.load(os.path.join(image_path, 'down.png')).get_width() * scale_factor),
                                            int(pygame.image.load(os.path.join(image_path, 'down.png')).get_height() * scale_factor))),
            'left': pygame.transform.scale(pygame.image.load(os.path.join(image_path, 'left.png')),
                                           (int(pygame.image.load(os.path.join(image_path, 'left.png')).get_width() * scale_factor),
                                            int(pygame.image.load(os.path.join(image_path, 'left.png')).get_height() * scale_factor))),
            'right': pygame.transform.scale(pygame.image.load(os.path.join(image_path, 'right.png')),
                                            (int(pygame.image.load(os.path.join(image_path, 'right.png')).get_width() * scale_factor),
                                             int(pygame.image.load(os.path.join(image_path, 'right.png')).get_height() * scale_factor)))
        }
        self.image = self.sprites[default_dir]  # Default direction
        # Random movement variables
        self.direction = 'down'
         # Start with a random offset for direction change
        self.last_direction_change = pygame.time.get_ticks() - random.randint(0, 2000)
        
        self.width = self.image.get_width()
        self.height = self.image.get_height() - 20
        # Create the rect using x, y, width, and height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.prompt = prompt
        self.chat_session = self.start_chat_session()
        self.selected_choice = 0  # Unique choice for each NPC
        self.dialogue_text = ""
        self.choice = None

    def update(self, in_dialogue):
        # Only randomize direction if not in dialogue
        if not in_dialogue:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_direction_change > 3000:  # Every 2 seconds
                self.randomize_direction()
                self.last_direction_change = current_time
    
    def randomize_direction(self):
        # Choose a random direction
        self.direction = random.choice(['up', 'down', 'left', 'right'])
        self.image = self.sprites[self.direction]

    def start_chat_session(self):
        model = genai.GenerativeModel(model_name="gemini-1.5-flash-8b", generation_config=generation_config)
        return model.start_chat(
            history=[
                {
                    "role": "user",
                    "parts": [self.prompt]
                },
                {
                    "role": "model",
                    "parts": [
                        "Welcome to my tavern, traveler. Care for a drink?\n```json\n{\"choice\": 0}\n```"
                    ],
                },
            ]
        )
        
    def get_dialogue(self,player_input):
        # Send player's input to LLM and update dialogue
        if not player_input:
            player_input = "ok"
        response = self.chat_session.send_message(player_input)
        print(response)
        
        # Extract the dialogue text
        dialogue_text = response.candidates[0].content.parts[0].text
        
        # Separate dialogue and JSON choice
        npc_dialogue = ""
        choice = 0  # Default choice value

        # Regular expression to match only the JSON block within the ```json``` markers
        json_pattern = re.compile(r'```json\s*(\{.*?\})\s*```', re.DOTALL)

        # Search for JSON block and remove it from dialogue text
        json_match = json_pattern.search(dialogue_text)
        if json_match:
            # Extract and parse JSON choice data
            try:
                choice_json = json.loads(json_match.group(1))
                choice = choice_json.get("choice", 0)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
            
            # Remove the JSON block from dialogue text
            npc_dialogue = json_pattern.sub('', dialogue_text).strip()
        else:
            npc_dialogue = dialogue_text.strip()

        # Update dialogue and clear player input
        self.dialogue_text = npc_dialogue

        # Print or display the player's selected choice
        print(f"Player choice: {choice}")
        self.choice = choice

        return npc_dialogue  # Return the dialogue text to be 
    
    def get_rect(self):
        return self.rect
    
    def face_player(self, player_x, player_y):
        # Determine direction to face based on player's position
        if abs(player_x - self.x) > abs(player_y - self.y):
            if player_x > self.x:
                self.image = self.sprites['right']
            else:
                self.image = self.sprites['left']
        else:
            if player_y > self.y:
                self.image = self.sprites['down']
            else:
                self.image = self.sprites['up']
