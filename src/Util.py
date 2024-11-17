import pygame
import json
import numpy as np

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
                "./spritesheet/main_character_in_battle/other_mage.json",
                "./spritesheet/Goblin/NormalGoblin/normalGob_Attack.json",
                "./spritesheet/Goblin/NormalGoblin/normalGob_Death.json",
                "./spritesheet/Goblin/NormalGoblin/normalGob_Idle.json",
                "./spritesheet/Goblin/NormalGoblin/normalGob_Walk.json",
                "./spritesheet/Goblin/NormalGoblin/normalGob_Stunt.json",
                "./spritesheet/VFX/mage_vfx/mage_heavy_vfx.json",
                "./spritesheet/VFX/mage_vfx/mage_light_vfx.json",
                "./spritesheet/VFX/mage_vfx/mage_debuff_vfx.json",
                "./spritesheet/VFX/mage_vfx/mage_explosion_vfx.json",
                "./spritesheet/VFX/mage_vfx/mage_true_vfx.json",
                "./spritesheet/VFX/ranger_vfx/ranger_heavy_vfx.json",
                "./spritesheet/VFX/ranger_vfx/ranger_light_vfx.json",
                "./spritesheet/VFX/ranger_vfx/ranger_shot_vfx.json",
                "./spritesheet/VFX/warrior_vfx/warrior_heavy_vfx.json",
                "./spritesheet/VFX/warrior_vfx/warrior_light_vfx.json",
                "./spritesheet/VFX/warrior_vfx/warrior_blood_vfx.json",
                "./spritesheet/VFX/warrior_vfx/warrior_strike_vfx.json",
                "./spritesheet/VFX/general_vfx/buff.json",
                "./spritesheet/VFX/general_vfx/debuff.json",
                "./spritesheet/VFX/general_vfx/dizzy.json",
                "./spritesheet/VFX/general_vfx/firefly.json",
                "./spritesheet/VFX/general_vfx/leavesFalling.json",
                "./spritesheet/VFX/general_vfx/MagicHIt.json",
                "./spritesheet/VFX/general_vfx/PhysicalHit.json",
                "./spritesheet/VFX/general_vfx/shield.json",
                "./spritesheet/VFX/general_vfx/heal.json",
                "./spritesheet/VFX/monster_vfx/monster_attack_vfx.json",
                "./spritesheet/Summon/ghost/ghost.json",
                "./spritesheet/Summon/ghost/ghost_summon.json",
                "./spritesheet/Effect/trap_idle.json",
                "./spritesheet/Effect/trap_attack.json",
                "./spritesheet/Effect/trap_summon.json",
                "./spritesheet/background/clock.json",
                "./spritesheet/background/dice.json",
                "./spritesheet/background/field.json",
                "./spritesheet/Summon/ghost/ghost.json",
                "./spritesheet/Summon/ghost/ghost_summon.json",
                "./spritesheet/Effect/trap_idle.json",
                "./spritesheet/Effect/trap_attack.json",
                "./spritesheet/Effect/trap_summon.json",
            ]
        )
        # self.spriteCollection["card_conf"] = self.loadCardConf("./cards/cards_corrected.json")

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
                        colorkey = animation_data.get("colorKey", -1)
                        tolerance = animation_data.get("tolerance", 5)
                        for sprite in animation_data["sprites"]:
                            if "Goblin" in animation_name:
                                scale = sprite.get("scale", 3) 
                            else:
                                scale = sprite.get("scale", 4) 
                            xSize = sprite.get('width', None)  # Use the new width
                            ySize = sprite.get('height', None)  # Use the new height
                            images.append(
                                mySpritesheet.image_at(
                                    sprite["x"],
                                    sprite["y"],
                                    scale,  
                                    colorkey,  
                                    tolerance,
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
                        offset_x = animation_data.get('offset_x', 0)
                        offset_y = animation_data.get('offset_y', 0)
                        interval_time = animation_data.get('interval_time', 0.5)
                        dic[animation_name] = Sprite(
                            None,
                            animation=Animation(animation_name, images, interval_time, looping=loop, idleSprite=idle_img, offset_x=offset_x, offset_y=offset_y)
                        )

                    resDict.update(dic)
                    continue
                else:
                    # Handling static sprites
                    for sprite in data["sprites"]:
                        colorkey = sprite.get("colorKey", -1)
                        tolerance = sprite.get("tolerance", 5)
                        xSize = sprite.get('width', None)  # Updated to use new width attribute
                        ySize = sprite.get('height', None)  # Updated to use new height attribute
                        scalefactor = sprite.get("scalefactor", 1)  # Updated to use scalefactor attribute
                        
                        dic[sprite["name"]] = Sprite(
                            mySpritesheet.image_at(
                                sprite["x"],
                                sprite["y"],
                                scalefactor,  # Using scalefactor from the sprite
                                colorkey,
                                tolerance,
                                xTileSize=xSize,
                                yTileSize=ySize,
                            ),
                        )
                    resDict.update(dic)

        return resDict

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
            print("REMINDER: The sprite sheet url is not assigned to", filename, "yet")

    def image_at(self, x, y, scalingfactor, colorkey, tolerance=5, xTileSize=16, yTileSize=16):
        """
        Extracts an image at a given position and removes background colors 
        within a given tolerance of the colorkey.
        """
        rect = pygame.Rect((x, y, xTileSize, yTileSize))
        image = pygame.Surface(rect.size, pygame.SRCALPHA)  # Use SRCALPHA for transparency
        image.blit(self.sheet, (0, 0), rect)

        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0, 0))[:3]  # Take only the RGB part
            else:
                colorkey = colorkey[:3]  # Ensure colorkey is always RGB
            
            if tolerance == 0:
                image.set_colorkey(colorkey)
            else:
                # Convert image to a NumPy array for pixel manipulation
                image_array = pygame.surfarray.array3d(image)  # RGB data
                alpha_array = pygame.surfarray.array_alpha(image)  # Alpha data
                
                # Calculate the difference between each pixel and the colorkey
                diff = np.abs(image_array - np.array(colorkey))
                within_tolerance = (diff[..., 0] <= tolerance) & \
                                (diff[..., 1] <= tolerance) & \
                                (diff[..., 2] <= tolerance)
                
                # Set alpha to 0 for pixels within the tolerance range
                alpha_array[within_tolerance] = 0
                
                # Create a new surface with updated alpha values
                for x in range(image.get_width()):
                    for y in range(image.get_height()):
                        alpha = alpha_array[x, y]
                        color = image_array[x, y]
                        image.set_at((x, y), (*color, alpha))

        # Scale the image
        return pygame.transform.scale(
            image, (xTileSize * scalingfactor, yTileSize * scalingfactor)
        )
        
class Animation:
    def __init__(self, name, images, interval_time, looping, idleSprite=None, offset_x=0, offset_y=0,):
        self.images = images
        self.timer = 0
        self.index = 0
        self.image = idleSprite if idleSprite else self.images[self.index]
        self.idleSprite = idleSprite
        self.offset_x = offset_x
        self.offset_y = offset_y
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
    
    def render(self, screen, x, y):
        screen.blit(self.image, (x, y))

    def is_finished(self):
        return self.finished
    
    def stop(self):
        self.index = 0
        self.finished = True
