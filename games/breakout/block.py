import pygame

from .sprite import Sprite
from .ball import Ball
from .geometry import Rectangle, Point

class Block(Sprite):
    def __init__(self, rect: pygame.Rect):
        self.rect = rect

        super().__init__(Rectangle(Point(rect.center.x, rect.center.y)))
    
    def draw(self, surface: pygame.Surface):
        pygame.draw.rect(surface, "black", self.rect)

    def bounce(self, ball: Ball):
        ball.direction *= -1
        self.kill()