class BuffConf():
    def __init__(self, name, duration, value, image=None):
        self.name = name
        self.duration = duration
        self.image = image
        self.value = value # [1,0,0,0] == [atk,def,spd,range]

class Buff():
    def __init__(self, conf):
        self.name = conf.name
        self.duration = conf.duration
        self.value = conf.value # [1,0,0,0] == [atk,def,spd,range]

    def apply(self, card):
        card.buffed_attack += self.value[0]
        card.buffed_defense += self.value[1]
        card.buffed_speed += self.value[2]
        card.buffed_range_end += self.value[3]
    
    def is_active(self):
        if self.duration == -1: # -1 means infinite duration
            return True
        elif self.duration > 0:
            return True
        else:
            return False

    def next_turn(self):
        if self.duration > 0:
            self.duration -= 1

    def render(self, screen):
        pass

    def update(self, dt, events):
        pass