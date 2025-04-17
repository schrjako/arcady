import pygame

from .sprite import Sprite

class Paddle(Sprite):
    def __init__(self, screen_width: int, y: float, width: float):
        self.screen_width = screen_width
        self.rect = pygame.Rect(screen_width / 2 - width, y, width, 10)

        super().__init__()

    def draw(self, surface):
        pygame.draw.rect(surface, "red", self.rect)