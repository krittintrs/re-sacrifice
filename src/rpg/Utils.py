import pygame
import json

def GenerateTiles(file_name, tile_width, tile_height, scale=3, colorkey=None):
    image = pygame.image.load(file_name)

    (img_width, img_height) = image.get_size()

    sheet_width = img_width//tile_width
    sheet_height = img_height//tile_height

    sheet_counter = 1
    tile_sheet = []

    for y in range(sheet_height):
        for x in range(sheet_width):
            tile = pygame.Surface((tile_width, tile_height))

            # surface, location, area of surface
            tile.blit(image, (0, 0), (x*tile_width, y*tile_height, tile_width, tile_height))

            # transparency
            if colorkey is not None:
                if colorkey == -1:
                    colorkey = image.get_at((0, 0))
                tile.set_colorkey(colorkey, pygame.RLEACCEL)

            tile = pygame.transform.scale(
                tile, (tile_width * scale, tile_height * scale)
            )

            tile_sheet.append(tile)

            sheet_counter += 1

    return tile_sheet

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

        self.looping = looping #default loop

        self.times_played = 0

    def Refresh(self):
        self.timer=0
        self.index = 0
        self.times_played=0

    def update(self, dt):
        # one time animation check (attacking)
        if self.looping is False and self.times_played>0:
            return

        self.timer = self.timer + dt

        if self.timer > self.interval_time:
            self.timer = self.timer % self.interval_time

            self.index = (self.index+1) % len(self.images)
            #print(self.index)

            if self.index == 0:
                self.times_played += 1

        self.image = self.images[self.index]

    def Idle(self):
        self.image = self.idleSprite


class Sprite:
    def __init__(self, image, animation=None):
        self.image = image
        self.animation = animation



class SpriteManager:
    def __init__(self):
        self.spriteCollection = self.loadSprites(
            [
                "./src/rpg/sprite/CharacterAnimation.json"
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
                            loop = sprite['loop']
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