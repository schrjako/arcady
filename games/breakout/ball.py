import pygame

from .sprite import Sprite


class Ball(Sprite):
	def __init__(self, radius: float, position: pygame.Vector2, direction: pygame.Vector2, speed: float):
		super().__init__()

		self.direction = direction
		self.speed = speed

		self.center = position
		self.radius = radius

	def draw(self, surface: pygame.Surface, glow_surf: pygame.Surface):
		for s in [surface, glow_surf]:
			pygame.draw.circle(s, (0, 191, 255), self.center, self.radius if s == surface else self.radius * 1.2)

	def update(self):
		self.center += self.direction * self.speed
