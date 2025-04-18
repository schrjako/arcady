import pygame

from .sprite import Sprite

def collide(a: Sprite, velocity: pygame.Vector2, b: Sprite) -> pygame.Vector2:
	...