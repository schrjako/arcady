import pygame

from abc import abstractmethod, ABCMeta

class Sprite(ABCMeta):
    def __init__(self):
        self.alive = True

    @abstractmethod
    def draw(self, surface: pygame.Surface) -> None:
        pass

    def kill(self):
        self.alive = False
        