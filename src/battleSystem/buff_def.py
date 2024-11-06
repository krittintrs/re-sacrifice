from src.resources import *

class BuffConf():
    def __init__(self, name, duration, value, imageName=None):
        self.name = name
        self.duration = duration
        self.value = value  # [1,0,0,0] == [atk,def,spd,range]
        self.imageName = imageName

DICE_ROLL_BUFF = {
    0: BuffConf('bonus_attack', 1, [1, 0, 0, 0], gBuffIcon_image_list['attack']),
    1: BuffConf('bonus_defense', 1, [0, 1, 0, 0], gBuffIcon_image_list['defense']),
    2: BuffConf('bonus_speed', 1, [0, 0, 1, 0], gBuffIcon_image_list['speed']),
}

CARD_BUFF = {
    'attack_boost': BuffConf('attack_boost', 2, [2, 0, 0, 0], gBuffIcon_image_list['attack']),
    'defense_boost': BuffConf('defense_boost', 2, [0, 2, 0, 0], gBuffIcon_image_list['defense']),
    'speed_boost': BuffConf('speed_boost', 2, [0, 0, 2, 0], gBuffIcon_image_list['speed']),
    'range_boost': BuffConf('range_boost', 2, [0, 0, 0, 2], gBuffIcon_image_list['range']),
    'perm_attack_boost': BuffConf('perm_attack_boost', -1, [1, 0, -1, 0], gBuffIcon_image_list['attack']),
    'perm_defense_boost': BuffConf('perm_defense_boost', -1, [-1, 1, 0, 0], gBuffIcon_image_list['defense']),
    'perm_speed_boost': BuffConf('perm_speed_boost', -1, [0, -1, 1, 0], gBuffIcon_image_list['speed']),
    'attack_debuff': BuffConf('attack_debuff', 2, [-2, 0, 0, 0], gBuffIcon_image_list['attack']),
    'defense_debuff': BuffConf('defense_debuff', 2, [0, -2, 0, 0], gBuffIcon_image_list['defense']),
    'speed_debuff': BuffConf('speed_debuff', 2, [0, 0, -2, 0], gBuffIcon_image_list['speed']),
    'range_debuff': BuffConf('range_debuff', 2, [0, 0, 0, -2], gBuffIcon_image_list['range']),
    'empower':BuffConf('empower', 2,[1, 1, 0, 0], None),
    'blood_buff':BuffConf('blood_buff', 1,[1, 0, 0, 0], gBuffIcon_image_list['attack']),
}