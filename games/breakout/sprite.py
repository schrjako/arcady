import pygame

from .geometry import Circle, Rectangle

from abc import abstractmethod, ABC

class Sprite(ABC):
    def __init__(self, hitbox: Circle | Rectangle):
        self.alive = True
        self.hitbox = hitbox

    @abstractmethod
    def draw(self, surface: pygame.Surface) -> None:
        pass

    def kill(self):
        self.alive = False 
