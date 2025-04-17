import pygame

from .sprite import Sprite

class Ball(Sprite):
    def __init__(self, radius: float, position: pygame.Vector2, direction: pygame.Vector2):
        self.position = position
        self.direction = direction
        self.radius = radius

        super().__init__()
    
    def draw(self, surface):
        pygame.draw.circle(surface, "blue", self.position, self.radius)