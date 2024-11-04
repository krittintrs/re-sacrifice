import pygame
import json
from src.EnumResources import EffectType
from src.battleSystem.Card import Card
from src.battleSystem.card_defs import CardConf
from src.battleSystem.Effect import Effect
from src.battleSystem.deck_defs import DeckConf
import copy

class Sprite:
    def __init__(self, image):
        self.image = image


class SpriteManager:
    def __init__(self):
        self.spriteCollection = {}
        self.spriteCollection = self.loadSprites(
            [
                "./spritesheet/BuffDebuff/BuffDebuff.json",
            ]
        )
        self.spriteCollection["card"] = self.loadCards("./cards/cards_corrected.json")
        self.spriteCollection["card_conf"] = self.loadCardConf("./cards/cards_corrected.json")


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
                        colorkey = -1
                    try:
                        xSize = sprite['width']
                        ySize = sprite['height']
                    except KeyError:
                        xSize, ySize = None, None
                    try: 
                        scalefactor = sprite["scalefactor"]
                    except KeyError:
                        scalefactor = 1
                    dic[sprite["name"]] = Sprite(
                        mySpritesheet.image_at(
                            sprite["x"],
                            sprite["y"],
                            scalefactor,
                            colorkey,
                            xTileSize=xSize,
                            yTileSize=ySize,
                        )
                    ).image
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

                # extract and create effects list for creating card
                temp_effect_dict = {}
                for type in card["effect"]:
                    temp_effect_dict[type] = []
                    if type == "buff":
                        for effect in card["effect"].get(type, []):
                            if effect:
                                match effect["type"]:
                                    case "attack":
                                        effect_type = EffectType.ATTACK
                                    case "move":
                                        effect_type = EffectType.MOVE
                                    case "self_buff":
                                        effect_type = EffectType.SELF_BUFF
                                    case "range_buff":
                                        effect_type = EffectType.RANGE_BUFF
                                    case "push":
                                        effect_type = EffectType.PUSH
                                    case "pull":
                                        effect_type = EffectType.PULL
                                    case "debuff":
                                        effect_type = EffectType.DEBUFF
                                    case "buff":
                                        effect_type = EffectType.BUFF
                                    case "cleanse":
                                        effect_type = EffectType.CLEANSE
                                    case "SandThrow":
                                        effect_type = EffectType.SAND_THROW
                                    case "AngelBlessing":
                                        effect_type = EffectType.ANGEL_BLESSING
                                    case "DestinyDraw":
                                        effect_type = EffectType.DESTINY_DRAW
                                    case "Reset":
                                        effect_type = EffectType.RESET
                                    case "Kamikaze":
                                        effect_type = EffectType.KAMIKAZE
                                    case "spawn":
                                        effect_type = EffectType.SPAWN
                                    case "heal":
                                        effect_type = EffectType.HEAL
                                    case "ditto":
                                        effect_type = EffectType.DITTO
                                    case "bloodSacrifice":
                                        effect_type = EffectType.BLOOD_SACRIFICE
                                    case "discard":
                                        effect_type = EffectType.DISCARD
                                temp_effect_dict[type].append(Effect(effect_type, effect["minRange"], effect["maxRange"], effect["buff"]))
                    else:
                        for effect in card["effect"].get(type, []):
                            if effect:
                                match effect["type"]:
                                    case "attack":
                                        effect_type = EffectType.ATTACK
                                    case "move":
                                        effect_type = EffectType.MOVE
                                    case "self_buff":
                                        effect_type = EffectType.SELF_BUFF
                                    case "range_buff":
                                        effect_type = EffectType.RANGE_BUFF
                                    case "push":
                                        effect_type = EffectType.PUSH
                                    case "pull":
                                        effect_type = EffectType.PULL
                                    case "debuff":
                                        effect_type = EffectType.DEBUFF
                                    case "buff":
                                        effect_type = EffectType.BUFF
                                    case "cleanse":
                                        effect_type = EffectType.CLEANSE
                                    case "SandThrow":
                                        effect_type = EffectType.SAND_THROW
                                    case "AngelBlessing":
                                        effect_type = EffectType.ANGEL_BLESSING
                                    case "DestinyDraw":
                                        effect_type = EffectType.DESTINY_DRAW
                                    case "Reset":
                                        effect_type = EffectType.RESET
                                    case "Kamikaze":
                                        effect_type = EffectType.KAMIKAZE
                                    case "spawn":
                                        effect_type = EffectType.SPAWN
                                    case "heal":
                                        effect_type = EffectType.HEAL
                                    case "ditto":
                                        effect_type = EffectType.DITTO
                                    case "bloodSacrifice":
                                        effect_type = EffectType.BLOOD_SACRIFICE
                                    case "discard":
                                        effect_type = EffectType.DISCARD
                                temp_effect_dict[type].append(Effect(effect_type, effect["minRange"], effect["maxRange"]))

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
        return cardDict
    

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
                for type in card["effect"]:
                    temp_effect_dict[type] = []
                    if type == "buff":
                        for effect in card["effect"].get(type, []):
                            if effect:
                                temp_effect_dict[type].append(Effect(effect["type"], effect["minRange"], effect["maxRange"], effect["buff"]))
                    else:
                        for effect in card["effect"].get(type, []):
                            if effect:
                                temp_effect_dict[type].append(Effect(effect["type"], effect["minRange"], effect["maxRange"]))

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
    

    
