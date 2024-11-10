from src.resources import *
from src.EnumResources import BuffType

class BuffConf:
    def __init__(self, name, description, duration, type, value, dot_damage, imageName=None):
        self.name = name
        self.description = description
        self.duration = duration
        self.type = type
        self.dot_damage = dot_damage
        self.value = value  # [1,0,0,0] == [atk,def,spd,range]
        self.imageName = imageName


DICE_ROLL_BUFF = {
    0: BuffConf("Bonus Attack Buff", "Bonus +1 ATK", 1, BuffType.DICE_ROLL, [1, 0, 0, 0], 0, gBuffIcon_image_list["attack"]),
    1: BuffConf("Bonus Defense Buff", "Bonus +1 DEF", 1, BuffType.DICE_ROLL, [0, 1, 0, 0], 0, gBuffIcon_image_list["defense"]),
    2: BuffConf("Bonus Speed Buff", "Bonus +1 SPD", 1, BuffType.DICE_ROLL, [0, 0, 1, 0], 0, gBuffIcon_image_list["speed"]),
}

CARD_BUFF = {
    "attack_boost": BuffConf(
        "Attack Boost", "+2 ATK", 2, BuffType.BUFF, [2, 0, 0, 0], 0, gBuffIcon_image_list["attack"]
    ),
    "defense_boost": BuffConf(
        "Defense Boost", "+2 DEF", 2, BuffType.BUFF, [0, 2, 0, 0], 0, gBuffIcon_image_list["defense"]
    ),
    "speed_boost": BuffConf(
        "Speed Boost", "+2 SPD", 2, BuffType.BUFF, [0, 0, 2, 0], 0, gBuffIcon_image_list["speed"]
    ),
    "range_boost": BuffConf(
        "Range Boost", "+1 RANGE", 2, BuffType.BUFF, [0, 0, 0, 1], 0, gBuffIcon_image_list["range"]
    ),
    "perm_attack_boost": BuffConf(
        "Permanent Attack Boost", "+1 ATK & -1 SPD", -1, BuffType.PERM_BUFF, [1, 0, -1, 0], 0, gBuffIcon_image_list["attack"]
    ),
    "perm_defense_boost": BuffConf(
        "Permanent Defense Boost", "+1 DEF & -1 ATK", -1, BuffType.PERM_BUFF, [-1, 1, 0, 0], 0, gBuffIcon_image_list["defense"]
    ),
    "perm_speed_boost": BuffConf(
        "Permanent Speed Boost", "+1 SPD & -1 DEF", -1, BuffType.PERM_BUFF, [0, -1, 1, 0], 0, gBuffIcon_image_list["speed"]
    ),
    "attack_debuff": BuffConf(
        "Attack Debuff", "-2 ATK", 2, BuffType.DEBUFF, [-2, 0, 0, 0], 0, gBuffIcon_image_list["attack"]
    ),
    "defense_debuff": BuffConf(
        "Defense Debuff", "-2 DEF", 2, BuffType.DEBUFF, [0, -2, 0, 0], 0, gBuffIcon_image_list["defense"]
    ),
    "speed_debuff": BuffConf(
        "Speed Debuff", "-2 SPD", 2, BuffType.DEBUFF, [0, 0, -2, 0], 0, gBuffIcon_image_list["speed"]
    ),
    "range_debuff": BuffConf(
        "Range Debuff", "-2 RANGE", 2, BuffType.DEBUFF, [0, 0, 0, -2], 0, gBuffIcon_image_list["range"]
    ),
    "empower": BuffConf(
        "Empower", "Empower (+1 ATK & +1 DEF)", 2, BuffType.EMPOWER, [1, 0, 0, 0], 0, gBuffIcon_image_list["defense"]
    ),
    "blood_buff": BuffConf(
        "Blood Buff", "Increase ATK by 30% of HP", 1, BuffType.BLOOD, [0, 0, 0, 0], 0, gBuffIcon_image_list["attack"]
    ),
    "crit+": BuffConf(
        "Critical+", "Increase Critical Chance to 4/6", 2, BuffType.CRIT_RATE, [0, 0, 0, 0], 0, gBuffIcon_image_list["critical"]
    ),
    "critical_buff": BuffConf(
        "Critical Damage", "Critical (x1.5 ATK)", 1, BuffType.CRIT_DMG, [0, 0, 0, 0], 0, gBuffIcon_image_list["critical"]
    ),
    "confuse": BuffConf(
        "Confusion", "Randomly Choose Tile", 1, BuffType.DEBUFF, [0, 0, 0, 0], 0, gBuffIcon_image_list["range"]
    ),
    'fire': BuffConf(
        'Fire', "Deal 1 damage per turn", 3, BuffType.DEBUFF, [0, 0, 0, 0], -1, gBuffIcon_image_list['debuff']
    ),
    'stop_movement': BuffConf(
        'Stop Movement', "Can not use move effect", 2, BuffType.STOP_MOVEMENT, [0, 0, 0, 0], 0, gBuffIcon_image_list['debuff']
    ),
    'stop_movement_2': BuffConf(
        'Stop Movement 2', "Can not use move effect", 10, BuffType.STOP_MOVEMENT, [0, 0, 0, 0], 0, gBuffIcon_image_list['debuff']
    ),
}
