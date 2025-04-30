import pygame

from .sprite import Sprite
from .ball import Ball
from .sound import SoundManager
from .particle import ParticleManager, Particle

from typing import override


class Block(Sprite):
	def __init__(self, rect: pygame.Rect, color: pygame.Color, sound: str):
		super().__init__()

		self.rect = rect

		self.color = color
		self.sound = sound

	@override
	def kill(self):
		self.alive = False

		# Go out with a flash 🤘
		def draw_glow(particle: Particle, surface: pygame.Surface, glow_surf: pygame.Surface):
			pygame.draw.rect(glow_surf, self.color, self.rect, border_radius=5)

		ParticleManager().spawn(8, draw_glow, [])

	def draw(self, surface: pygame.Surface, glow_surf: pygame.Surface):
		pygame.draw.rect(surface, self.color, self.rect, border_radius=5)
		pygame.draw.rect(glow_surf, self.color, self.rect.scale_by(0.4, 0.4), border_radius=5)
		pygame.draw.rect(surface, self.color - pygame.Color(100, 100, 100), self.rect, width=2, border_radius=5)

	def bounce(self, ball: Ball) -> bool:
		def inside(a: float, b: float, c: float) -> bool:
			return a < b < c or c < b < a

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
				SoundManager().play(self.sound)
				return True

		for i in range(len(points)):
			if (points[i] - ball.center).length() <= ball.radius:
				ball.direction.reflect_ip(pygame.Vector2(points[i] - ball.center))
				ball.bounce()
				SoundManager().play(self.sound)
				return True

		return False
