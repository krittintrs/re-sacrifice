class Buff():
    def __init__(self, name, active_time, entity):
        self.name = name
        self.active_time = active_time
        self.buff_entity = entity

    def apply(self):
        pass

    def render(self, screen):
        pass

    def update(self, dt, events):
        pass    
