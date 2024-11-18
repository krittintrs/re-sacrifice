import json
from src.Util import SpriteSheet, Sprite
from src.EnumResources import EffectType, CardType, VFXType, AnimationType
from src.battleSystem.Effect import Effect


class CardConf:
    def __init__(self, id, name, class_, type, vfx_type, animation_type, description, image, attack, defense, speed, range_start, range_end, beforeEffect = [], mainEffect = [], afterEffect = []):
        # For Render
        self.id = id
        self.class_ = class_
        self.type = type
        self.vfx_type = vfx_type
        self.animation_type = animation_type
        self.name = name
        self.description = description
        self.image = image

        # Card Stats
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.range_start = range_start
        self.range_end = range_end

        # Card Effects
        self.beforeEffect = beforeEffect # list of Effects
        self.mainEffect = mainEffect
        self.afterEffect = afterEffect

    def display_attributes(self):
        print(f"ID: {self.id}")
        print(f"Class: {self.class_}")
        print(f"Type: {self.type}")
        print(f"Name: {self.name}")
        print(f"Description: {self.description}")
        print(f"Image: {self.image}")
        print(f"Attack: {self.attack}")
        print(f"Defense: {self.defense}")
        print(f"Speed: {self.speed}")
        print(f"Range Start: {self.range_start}")
        print(f"Range End: {self.range_end}")
        
        # Printing effects
        print("Before Effects:")
        for effect in self.beforeEffect:
            print(f"  - {effect}")
        
        print("Main Effects:")
        for effect in self.mainEffect:
            print(f"  - {effect}")
        
        print("After Effects:")
        for effect in self.afterEffect:
            print(f"  - {effect}")

def loadCardConf(url):
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
            try: 
                card_type = CardType(card["type"])
            except KeyError:
                card_type = None
            try:
                vfx_type = VFXType(card["vfxType"])
            except KeyError:
                vfx_type = None
            try:
                animation_type = AnimationType(card["animationType"])
            except KeyError:
                animation_type = None

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
                        try:
                            effect_spawn = effect["spawn"]
                        except KeyError:
                            effect_spawn = None
                        temp_effect_dict[effectPeriod].append(Effect(effect_type, effect["minRange"], effect["maxRange"], effect_buff, effect_spawn))
                        # print(f"{effect_type}\t{effect_buff}")

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
                type=card_type,
                vfx_type=vfx_type,
                animation_type=animation_type,
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

CARD_DEFS = loadCardConf("./cards/cards_corrected.json")

