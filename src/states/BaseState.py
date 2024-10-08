from abc import ABC, abstractmethod

class BaseState(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def Enter(self, params):
        pass

    @abstractmethod
    def Exit(self):
        pass

    @abstractmethod
    def update(self, dt, events):
        pass

    @abstractmethod
    def render(self, screen):
        pass