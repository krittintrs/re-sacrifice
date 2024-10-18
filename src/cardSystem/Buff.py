class Buff():
    def __init__(self, name, duration, value):
        self.name = name
        self.duration = duration
        self.value = value # [1,0,0,0] == [atk,def,spd,range]

    def apply(self, entity):
        entity.attack += self.value[0]
        entity.defense += self.value[1]
        entity.speed += self.value[2]
        entity.range += self.value[3]
    
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