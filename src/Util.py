import pygame
import json
from src.EnumResources import EffectType
from src.battleSystem.card_defs import CardConf
from src.battleSystem.Effect import Effect
from src.battleSystem.deck_defs import DeckConf

class Sprite:
    def __init__(self, image, animation=None):
        self.image = image
        self.animation = animation


class SpriteManager:
    def __init__(self):
        self.spriteCollection = {}
        self.spriteCollection = self.loadSprites(
            [
                "./spritesheet/BuffDebuff/BuffDebuff.json",
                "./spritesheet/main_character_in_battle/warrior.json",
                "./spritesheet/main_character_in_battle/ranger.json",
                "./spritesheet/main_character_in_battle/mage.json",
                "./spritesheet/main_character_in_battle/other_warrior.json",
                "./spritesheet/main_character_in_battle/other_ranger.json",
                "./spritesheet/main_character_in_battle/other_mage.json"
            ]
        )
        self.spriteCollection["card_conf"] = self.loadCardConf("./cards/cards_corrected.json")

    def loadSprites(self, urlList, shrink_scale=1):
        resDict = {}  # result dictionary
        for url in urlList:
            with open(url) as jsonData:
                data = json.load(jsonData)
                mySpritesheet = SpriteSheet(data["spriteSheetURL"])
                dic = {}

                # Handling animations
                if data["type"] == "animation":
                    # Loop through each animation in the animations section
                    for animation_name, animation_data in data["animations"].items():
                        images = []
                        for sprite in animation_data["sprites"]:
                            xSize = sprite.get('width', None)  # Use the new width
                            ySize = sprite.get('height', None)  # Use the new height
                            images.append(
                                mySpritesheet.image_at(
                                    sprite["x"],
                                    sprite["y"],
                                    sprite.get("scale", 4),  # Use the scale from the sprite or default to 1
                                    colorkey=-1,  # Default color key if not provided
                                    xTileSize=xSize,
                                    yTileSize=ySize,
                                )
                            )
                        # Check for idle image if necessary
                        idle_img = None
                        if 'idle_image' in animation_data:  # This may not be in your current JSON, but keep it for future flexibility
                            idle_info = animation_data['idle_image']
                            idle_img = mySpritesheet.image_at(
                                idle_info["x"],
                                idle_info["y"],
                                idle_info.get("scale", 5),
                                colorkey=-1,
                                xTileSize=xSize,
                                yTileSize=ySize
                            )
                        # Handle loop setting
                        loop = animation_data.get('loop', 'true').lower() == 'true'  # Convert string to boolean, default to True if not specified
                        dic[animation_name] = Sprite(
                            None,
                            animation=Animation(images, looping=loop, idleSprite=idle_img, interval_time=sprite.get("interval_time", 1)),
                        )

                    resDict.update(dic)
                    continue
                else:
                    # Handling static sprites
                    for sprite in data["sprites"]:
                        colorkey = sprite.get("colorKey", -1)
                        xSize = sprite.get('width', None)  # Updated to use new width attribute
                        ySize = sprite.get('height', None)  # Updated to use new height attribute
                        scalefactor = sprite.get("scalefactor", 1)  # Updated to use scalefactor attribute
                        
                        dic[sprite["name"]] = Sprite(
                            mySpritesheet.image_at(
                                sprite["x"],
                                sprite["y"],
                                scalefactor,  # Using scalefactor from the sprite
                                colorkey,
                                xTileSize=xSize,
                                yTileSize=ySize,
                            ),
                        )
                    resDict.update(dic)

        return resDict

    def loadCardConf(self, url):
        card_conf= {} 
        with open(url) as jsonData:
            data = json.load(jsonData)
            mySpritesheet = SpriteSheet(data["spriteSheetURL"])
            for card in data["cards"]:
                try:
                    colorkey = card["sprite"]["colorKey"]
                except KeyError:
                    colorkey = None
                try:
                    xSize = card.get('xsize', data['size'][0])  # If xsize is not present, use default size
                    ySize = card.get('ysize', data['size'][1])  # If ysize is not present, use default size
                except KeyError:
                    xSize, ySize = data['size']

                # extract and create effects list for creating card
                temp_effect_dict = {}
                for effectPeriod in card["effect"]:
                    temp_effect_dict[effectPeriod] = []
                    for effect in card["effect"].get(effectPeriod, []):
                        if effect:
                            try:
                                effect_type = EffectType(effect["type"])
                            except ValueError:
                                print(f"Unknown effect type: {effect['type']}")
                                continue
                            try:
                                effect_buff = effect["buff"]
                            except KeyError:
                                effect_buff = None
                            temp_effect_dict[effectPeriod].append(Effect(effect_type, effect["minRange"], effect["maxRange"], effect_buff))
                            print(effect_type, effect_buff)

                # Create the Card object for each card entry
                card_conf[card["name"]] = CardConf(
                    name=card["name"],
                    description=card.get("description", ""),  # Use empty string if description is missing
                    image=Sprite(
                        mySpritesheet.image_at(
                            card["sprite"]["x"],
                            card["sprite"]["y"],
                            card["sprite"]["scalefactor"],
                            (255,0,255),
                            xTileSize=xSize,
                            yTileSize=ySize,
                        )
                    ).image,
                    id=card["id"],
                    class_=card["class"],
                    type=card["type"],
                    speed=card["speed"],
                    attack=card["attack"],  
                    defense=card["defense"],
                    range_start=card["range_start"],
                    range_end=card["range_end"],
                    beforeEffect=temp_effect_dict["beforeEffect"],
                    mainEffect=temp_effect_dict["mainEffect"],
                    afterEffect=temp_effect_dict["afterEffect"]
                )
        return card_conf

class SpriteSheet:
    def __init__(self, filename):
        try:
            self.sheet = pygame.image.load(filename)
            if not self.sheet.get_alpha():
                self.sheet.set_colorkey((0, 0, 0))
        except pygame.error:
            print("Unable to load spritesheet image:", filename)
            raise SystemExit
        except Exception as error:
            print("REMINDER: The sprite sheet url is not assigned to card yet")

    def image_at(self, x, y, scalingfactor, colorkey=None, xTileSize=16, yTileSize=16):
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
    
class DeckLoader():
    def __init__(self):
        self.deck_conf = self.loadDeck()

    def loadDeck(self):
        url = "./cards/decks.json"
        deck_conf = {}
        with open(url) as jsonData:
            data = json.load(jsonData)
            for deck_type in data:
                deck_conf[deck_type] = DeckConf(data[deck_type])
        
        return deck_conf
    
class Animation:
    def __init__(self, images, looping, idleSprite=None, interval_time=0.15, name="Animation"):
        self.images = images
        self.timer = 0
        self.index = 0
        self.image = idleSprite if idleSprite else self.images[self.index]
        self.idleSprite = idleSprite
        self.interval_time = interval_time
        self.looping = looping
        self.times_played = 0
        self.finished = False
        self.name = name  # Identifier for debugging

    def get_frames(self):
        return self.images

    def Refresh(self):
        self.timer = 0
        self.index = 0
        self.times_played = 0
        self.finished = False

    def update(self, dt):
        self.timer += dt
        
        if self.timer >= self.interval_time:
            self.index += 1
            if self.index >= len(self.images):
                self.times_played += 1
                if self.looping:
                    self.index = 0
                else:
                    self.index = len(self.images) - 1
                    self.finished = True
            self.image = self.images[self.index]

    def is_finished(self):
        return self.finished