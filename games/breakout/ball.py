import pygame

from .sprite import Sprite
from .geometry import Circle, Point

class Ball(Sprite):
    def __init__(self, radius: float, position: Point, direction: pygame.Vector2):
        self.position = position
        self.direction = direction
        self.radius = radius

        super().__init__(Circle(self.position, self.radius))
    
    def draw(self, surface: pygame.Surface):
        pygame.draw.circle(surface, "blue", self.position.get_tuple(), self.radius)