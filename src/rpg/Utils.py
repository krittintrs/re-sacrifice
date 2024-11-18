import time
import pygame
import json
from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT
from src.resources import gFont_list

response_button_rect = pygame.Rect(950, 470, 125, 40)
close_button_rect = pygame.Rect(1100, 470, 125, 40)

def wrap_text(text, font, max_width):
    # Split text into lines based on width constraints
    words = text.split()
    lines = []
    current_line = ""
    
    for word in words:
        # Test adding this word to the current line
        test_line = f"{current_line} {word}".strip()
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word

    # Append any remaining text to lines
    if current_line:
        lines.append(current_line)
    
    return lines

def render_dialogue(screen,npc,dialogue_text,blink,last_blink_time,player_input):
            
    # Extend dialogue box to full width
    dialogue_box_x = 50
    dialogue_box_width = SCREEN_WIDTH - 100
    dialogue_box_height = 150
    dialogue_box_y = SCREEN_HEIGHT - 200

    # Render dialogue box
    pygame.draw.rect(screen, (200, 200, 200), (dialogue_box_x, dialogue_box_y, dialogue_box_width, dialogue_box_height))
    font = gFont_list["title"]
    
    npc_image = pygame.image.load(npc.image_path+"/Face.png").convert_alpha()
    npc_image = pygame.transform.scale(npc_image, (400, 400))  # Resize NPC image as needed
    screen.blit(npc_image, (dialogue_box_x + dialogue_box_width - 400, dialogue_box_y - 400))  # Position image above dialogue box
    
    # Render NPC name box above the dialogue box
    name_box_height = 40
    name_box_width = 100
    name_box_y = dialogue_box_y - name_box_height - 10
    pygame.draw.rect(screen, (220, 220, 220), (dialogue_box_x, name_box_y, name_box_width, name_box_height))
    name_font = gFont_list["header"]
    npc_name_surface = name_font.render(npc.name, True, (0, 0, 0))
    # Center the NPC name within the name box
    name_x = dialogue_box_x + (name_box_width - npc_name_surface.get_width()) // 2
    screen.blit(npc_name_surface, (name_x, name_box_y +10))
    
    # Handle multiline dialogue text wrapping
    dialogue_text_lines = wrap_text(dialogue_text, font, dialogue_box_width - 20)
    line_height = 30
    for i, line in enumerate(dialogue_text_lines):
        dialogue_surface = font.render(line, True, (0, 0, 0))
        screen.blit(dialogue_surface, (dialogue_box_x + 20, dialogue_box_y + 20 + i * line_height))
        
    # Toggle blinking for cursor
    current_time = time.time()
    if current_time - last_blink_time > 0.5:  # Blink every 0.5 seconds
        blink = not blink
        last_blink_time = current_time
    
    # Display player input with blinking cursor
    input_text = player_input
    if blink:
        input_text += "_"  # Add blinking cursor
    player_input_surface = font.render(input_text, True, (0, 0, 255))
    screen.blit(player_input_surface, (70, SCREEN_HEIGHT - 100))

    # # Draw "Respond" button
    # pygame.draw.rect(screen, (100, 200, 100), response_button_rect)
    # respond_text = font.render("Respond", True, (255, 255, 255))
    # screen.blit(respond_text, (response_button_rect.x + 10, response_button_rect.y + 10))

    # # Draw "Close" button
    # pygame.draw.rect(screen, (200, 100, 100), close_button_rect)
    # close_text = font.render("Close", True, (255, 255, 255))
    # screen.blit(close_text, (close_button_rect.x + 10, close_button_rect.y + 10))

def render_quests(screen,quests):
    font = gFont_list["header"]
    # Set background dimensions
    background_width = 280
    background_height = 40 + len(quests) * 20
    background_x = SCREEN_WIDTH - background_width - 100
    background_y = 10

    # Draw the background with semi-transparency
    background_surface = pygame.Surface((background_width, background_height))
    background_surface.set_alpha(150)  # 150 for semi-transparency
    background_surface.fill((0, 0, 0))  # Black background
    screen.blit(background_surface, (background_x, background_y))

    # Display "Quest" title
    quest_title_surface = font.render("Quest", True, (255, 255, 255))
    screen.blit(quest_title_surface, (background_x + 10, background_y + 10))

    # Display each quest below the title
    for i, quest in enumerate(quests):
        quest_text_surface = font.render(quests[quest], True, (255, 255, 255))
        screen.blit(quest_text_surface, (background_x + 10, background_y + 40 + i * 20))

def render_topics(screen,topics):
    font = gFont_list["title"]
    # Set background dimensions
    topic_background_width = 560
    topic_background_height = 60 + len(topics) * 40
    topic_background_x = SCREEN_WIDTH - topic_background_width - 620
    topic_background_y = 10

    # Draw the background with semi-transparency
    topic_background_surface = pygame.Surface((topic_background_width, topic_background_height))
    topic_background_surface.set_alpha(150)  # 150 for semi-transparency
    topic_background_surface.fill((0, 0, 0))  # Black background
    screen.blit(topic_background_surface, (topic_background_x, topic_background_y))

    # Display "Quest" title
    topic_title_surface = font.render("Suggested Conversation Topics", True, (255, 255, 255))
    screen.blit(topic_title_surface, (topic_background_x + 10, topic_background_y + 10))

    # Display each quest below the title
    for i, topic in enumerate(topics):
        topic_text_surface = font.render("- "+topics[topic], True, (255, 255, 255))
        screen.blit(topic_text_surface, (topic_background_x + 10, topic_background_y + 60 + i * 50))
        
def render_interaction_dialogue(screen, dialogue_text,enter_action_text="Enter", escape_action_text="Escape"):
    # Extend dialogue box to full width
    dialogue_box_x = 50
    dialogue_box_width = SCREEN_WIDTH - 100
    dialogue_box_height = 150
    dialogue_box_y = SCREEN_HEIGHT - 200

    # Render dialogue box
    pygame.draw.rect(screen, (200, 200, 200), (dialogue_box_x, dialogue_box_y, dialogue_box_width, dialogue_box_height))
    font = gFont_list["title"]

    # Handle multiline dialogue text wrapping
    dialogue_text_lines = wrap_text(dialogue_text, font, dialogue_box_width - 20)
    line_height = 30
    for i, line in enumerate(dialogue_text_lines):
        dialogue_surface = font.render(line, True, (0, 0, 0))
        screen.blit(dialogue_surface, (dialogue_box_x + 20, dialogue_box_y + 20 + i * line_height))

    return None  # No action yet

class Animation:
    def __init__(self, images, idleSprite=None, looping=True, interval_time=0.15):
        self.images = images
        self.timer = 0
        self.index = 0
        if idleSprite is None:
            self.image = self.images[self.index]
        else:
            self.image = idleSprite
        self.idleSprite = idleSprite

        self.interval_time = interval_time
        self.finished = False
        self.looping = looping #default loop

        self.times_played = 0

    def Refresh(self):
        self.timer=0
        self.index = 0
        self.times_played=0
        self.finished = False

    def update(self, dt):
        # old version of update

        # if self.looping is False and self.times_played>0:
        #     return

        # self.timer = self.timer + dt

        # if self.timer > self.interval_time:
        #     self.timer = self.timer % self.interval_time

        #     self.index = (self.index+1) % len(self.images)
        #     #print(self.index)

        #     if self.index == 0:
        #         self.times_played += 1

        # self.image = self.images[self.index]

        self.timer += dt
        if self.timer >= self.interval_time and not self.finished:
            self.index += 1
            self.timer = 0
            if self.index >= len(self.images):
                self.times_played += 1
                if self.looping:
                    self.index = 0
                else:
                    self.finished = True
                    self.index = 0
            self.image = self.images[self.index]
        elif self.finished:
            self.index = 0

    def Idle(self):
        self.image = self.idleSprite

    def is_finished(self):
        return self.finished
    
    def stop(self):
        self.index = 0
        self.finished = True


class Sprite:
    def __init__(self, image, animation=None):
        self.image = image
        self.animation = animation



class SpriteManager:
    def __init__(self):
        self.spriteCollection = self.loadSprites(
            [
                "./src/rpg/sprite/CharacterAnimation.json",
                "./src/rpg/sprite/mageAnimation.json",
                "./src/rpg/sprite/warriorAnimation.json",
                "./src/rpg/sprite/rangerAnimation.json"
            ]
        )

    def loadSprites(self, urlList, shrink_scale=1):
        resDict = {}
        for url in urlList:
            with open(url) as jsonData:
                data = json.load(jsonData)
                mySpritesheet = SpriteSheet(data["spriteSheetURL"])
                dic = {}

                if data["type"] == "animation":
                    for sprite in data["sprites"]:
                        images = []
                        for image in sprite["images"]:
                            try:
                                xSize = sprite['xsize']
                                ySize = sprite['ysize']
                            except KeyError:
                                xSize, ySize = data['size']
                            images.append(
                                mySpritesheet.image_at(
                                    image["x"],
                                    image["y"],
                                    image["scale"],
                                    colorkey=-1, #sprite["colorKey"],
                                    xTileSize=xSize,
                                    yTileSize=ySize,
                                )
                            )
                        try:
                            idle_info = sprite['idle_image']
                            idle_img = mySpritesheet.image_at(
                                idle_info["x"],
                                idle_info["y"],
                                idle_info["scale"],
                                colorkey=-1,
                                xTileSize=xSize,
                                yTileSize=ySize
                            )
                        except KeyError:
                            idle_img = None
                        try:
                            loop = sprite['loop'].lower() == 'true'
                        except KeyError:
                            loop = True

                        dic[sprite["name"]] = Sprite(
                            None,
                            animation=Animation(images, idleSprite=idle_img, looping=loop, interval_time=sprite["interval_time"]),
                        )

                    resDict.update(dic)
                    continue
                else:
                    for sprite in data["sprites"]:
                        try:
                            colorkey = sprite["colorKey"]
                        except KeyError:
                            colorkey = None
                        try:
                            xSize = sprite['xsize']
                            ySize = sprite['ysize']
                        except KeyError:
                            xSize, ySize = data['size']
                        dic[sprite["name"]] = Sprite(
                            mySpritesheet.image_at(
                                sprite["x"],
                                sprite["y"],
                                sprite["scalefactor"],#//shrink_scale,
                                colorkey,
                                xTileSize=xSize,
                                yTileSize=ySize,
                            ),
                        )
                    resDict.update(dic)
                    continue
        return resDict

class SpriteSheet(object):
    def __init__(self, filename):
        try:
            self.sheet = pygame.image.load(filename)
            self.sheet = pygame.image.load(filename)
            if not self.sheet.get_alpha():
                self.sheet.set_colorkey((0, 0, 0))
        except pygame.error:
            print("Unable to load spritesheet image:", filename)
            raise SystemExit

    def image_at(self, x, y, scalingfactor, colorkey=None,
                 xTileSize=16, yTileSize=16):
        rect = pygame.Rect((x, y, xTileSize, yTileSize))
        image = pygame.Surface(rect.size)
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return pygame.transform.scale(
            image, (xTileSize * scalingfactor, yTileSize * scalingfactor)
        )