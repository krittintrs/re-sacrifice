class Buff():
    def __init__(self, name, duration, value):
        self.name = name
        self.duration = duration
        self.value = value # [1,0,0,0] == [atk,def,spd,range]

    def apply(self):
        pass

    def render(self, screen):
        pass

    def update(self, dt, events):
        pass

    # if timeout return true
    def is_active(self):
        self.duration -= 1
        if self.duration >= 0:
            return True
        else:
            return False

