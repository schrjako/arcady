import pygame

from .sprite import Sprite
from .ball import Ball

from typing import override


class Block(Sprite):
	def __init__(self, rect: pygame.Rect, color: pygame.Color):
		super().__init__()

		self.fading: int = 0

		self.rect = rect

		self.color = color

	@override
	def kill(self):
		self.alive = False
		self.fading = 8

	@override
	def is_alive(self) -> bool:
		return self.alive or self.fading > 0

	def draw(self, surface: pygame.Surface, glow_surf: pygame.Surface):
		if not self.fading:
			pygame.draw.rect(surface, self.color, self.rect, border_radius=5)
			pygame.draw.rect(glow_surf, self.color, self.rect.scale_by(0.4, 0.4), border_radius=5)
			pygame.draw.rect(surface, self.color - pygame.Color(100, 100, 100), self.rect, width=2, border_radius=5)

		else:
			pygame.draw.rect(glow_surf, self.color, self.rect, border_radius=5)
			self.fading -= 1

	def bounce(self, ball: Ball) -> bool:
		def inside(a: float, b: float, c: float) -> bool:
			return a < b < c or c < b < a

		if self.alive:
			points = [
				pygame.Vector2(self.rect.left, self.rect.top),
				pygame.Vector2(self.rect.left, self.rect.bottom),
				pygame.Vector2(self.rect.right, self.rect.bottom),
				pygame.Vector2(self.rect.right, self.rect.top),
			]

			for i in range(len(points)):
				line = [points[i], points[(i + 1) % len(points)]]

				move = (line[0] - line[1]).normalize().rotate(-90)

				p = line[1] + move * ball.radius

				if inside(p.x, ball.center.x, line[0].x) and inside(p.y, ball.center.y, line[0].y):
					ball.direction.reflect_ip((line[0] - line[1]).rotate(90))
					ball.bounce()
					return True

			for i in range(len(points)):
				if (points[i] - ball.center).length() <= ball.radius:
					ball.direction.reflect_ip(pygame.Vector2(points[i] - ball.center))
					ball.bounce()
					return True

		return False
