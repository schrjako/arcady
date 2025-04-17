import pygame

from .sprite import Sprite
from .ball import Ball

class Block(Sprite):
    def __init__(self, rect: pygame.Rect):
        self.rect = rect

        super().__init__()
    
    def draw(self, surface):
        pygame.draw.rect(surface, "black", self.rect)

    def bounce(self, ball: Ball):
        ball.direction *= -1
        self.kill()