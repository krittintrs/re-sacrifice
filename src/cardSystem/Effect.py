class Effect():
    def __init__(self, type, minRange, maxRange, buff = None):
        self.type = type
        self.minRange = minRange
        self.maxRange = maxRange
        self.buff = buff

    def apply(self):
        pass

    def render(self, screen):
        pass

    def update(self, dt, events):
        pass

