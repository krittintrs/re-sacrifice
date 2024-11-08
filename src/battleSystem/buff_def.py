from src.resources import *

class BuffConf():
    def __init__(self, name, duration, value, imageName=None):
        self.name = name
        self.duration = duration
        self.value = value  # [1,0,0,0] == [atk,def,spd,range]
        self.imageName = imageName

DICE_ROLL_BUFF = {
    0: BuffConf('Bonus +1 ATK', 1, [1, 0, 0, 0], gBuffIcon_image_list['attack']),
    1: BuffConf('Bonus +1 DEF', 1, [0, 1, 0, 0], gBuffIcon_image_list['defense']),
    2: BuffConf('Bonus +1 SPD', 1, [0, 0, 1, 0], gBuffIcon_image_list['speed']),
}

CARD_BUFF = {
    'attack_boost': BuffConf('+2 ATK', 2, [2, 0, 0, 0], gBuffIcon_image_list['attack']),
    'defense_boost': BuffConf('+2 DEF', 2, [0, 2, 0, 0], gBuffIcon_image_list['defense']),
    'speed_boost': BuffConf('+2 SPD', 2, [0, 0, 2, 0], gBuffIcon_image_list['speed']),
    'range_boost': BuffConf('+2 RANGE', 2, [0, 0, 0, 2], gBuffIcon_image_list['range']),
    'perm_attack_boost_1': BuffConf('+1 ATK', -1, [1, 0, 0, 0], gBuffIcon_image_list['attack']),
    'perm_attack_boost_2': BuffConf('-1 SPD', -1, [0, 0, -1, 0], gBuffIcon_image_list['speed']),
    'perm_defense_boost_1': BuffConf('+1 DEF', -1, [0, 1, 0, 0], gBuffIcon_image_list['defense']),
    'perm_defense_boost_2': BuffConf('-1 ATK', -1, [-1, 0, 0, 0], gBuffIcon_image_list['attack']),
    'perm_speed_boost_1': BuffConf('+1 SPD', -1, [0, 0, 1, 0], gBuffIcon_image_list['speed']),
    'perm_speed_boost_2': BuffConf('-1 DEF', -1, [0, -1, 0, 0], gBuffIcon_image_list['defense']),
    'attack_debuff': BuffConf('-2 ATK', 2, [-2, 0, 0, 0], gBuffIcon_image_list['attack']),
    'defense_debuff': BuffConf('-2 DEF', 2, [0, -2, 0, 0], gBuffIcon_image_list['defense']),
    'speed_debuff': BuffConf('-2 SPD', 2, [0, 0, -2, 0], gBuffIcon_image_list['speed']),
    'range_debuff': BuffConf('-2 RANGE', 2, [0, 0, 0, -2], gBuffIcon_image_list['range']),
    'empower_1': BuffConf('Empower (+1 ATK)', 2, [1, 0, 0, 0], gBuffIcon_image_list['attack']),
    'empower_2': BuffConf('Empower (+1 DEF)', 2, [0, 1, 0, 0], gBuffIcon_image_list['defense']),
    'blood_buff': BuffConf('Blood Buff', 1, [0, 0, 0, 0], gBuffIcon_image_list['attack']),
    'crit+': BuffConf('Critical+ (4/6 chance)', 2,[0, 0, 0, 0], gBuffIcon_image_list['critical']),
    'critical_buff': BuffConf('Critical (x1.5 ATK)', 1,[0, 0, 0, 0], gBuffIcon_image_list['critical']),
}