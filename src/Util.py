import pygame
import json
from src.cardSystem.Card import Card

class Sprite:
    def __init__(self, image):
        self.image = image


class SpriteManager:
    def __init__(self):
        self.spriteCollection = {}
        # self.spriteCollection = self.loadSprites(
        #     [
        #         "./sprite/MiddlePaddle.json",
        #         "./sprite/SmallPaddle.json",
        #         "./sprite/Brick.json",
        #         "./sprite/Ball.json",
        #         "./sprite/Heart.json",
        #         "./sprite/Arrow.json",
        #     ]
        # )
        self.spriteCollection["card"] = self.loadCards("./cards/cards.json")

    # copy from breakout
    def loadSprites(self, urlList):
        resDict = {} #result dictionary
        for url in urlList:
            with open(url) as jsonData:
                data = json.load(jsonData)
                mySpritesheet = SpriteSheet(data["spriteSheetURL"])
                dic = {}
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
                            sprite["scalefactor"],
                            colorkey,
                            xTileSize=xSize,
                            yTileSize=ySize,
                        )
                    )
                resDict.update(dic)
                continue
        return resDict
    
    def loadCards(self, url):
        cardDict = {} 
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

                # Create the Card object for each card entry
                cardDict[card["name"]] = Card(
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
                    speed=card["speed"],
                    attack=card["attack"],  
                    defense=card["defense"],  
                    range_start=card["range_start"],
                    range_end=card["range_end"],
                    beforeEffect=card["effect"].get("beforeEffect", {}),
                    mainEffect=card["effect"].get("mainEffect", {}),
                    afterEffect=card["effect"].get("afterEffect", {})
                )
        return cardDict

class SpriteSheet(object):
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
