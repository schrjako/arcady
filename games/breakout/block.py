import pygame

from .sprite import Sprite
from .ball import Ball, BallManager
from .sound import SoundManager
from .particle import ParticleManager, Particle

from typing import override, Literal
import random


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
		# pygame.draw.rect(glow_surf, self.color, self.rect.scale_by(0.4, 0.4), border_radius=5)
		pygame.draw.rect(surface, self.color - pygame.Color(100, 100, 100, 0), self.rect, width=2, border_radius=5)

	def on_hit(self, ball: Ball, side_or_corner: Literal[0, 1], which: int):
		"""
		0 for side, 1 for corner
		which: 0: top side or top left corner, counterclockwise
		"""
		ball.bounce_anim()
		SoundManager().play(self.sound)
		self.kill()

	def bounce(self, ball: Ball) -> bool:
		def inside(a: float, b: float, c: float) -> bool:
			return a < b < c or c < b < a

		points = (
			pygame.Vector2(self.rect.left, self.rect.top),
			pygame.Vector2(self.rect.left, self.rect.bottom),
			pygame.Vector2(self.rect.right, self.rect.bottom),
			pygame.Vector2(self.rect.right, self.rect.top),
		)

		for i in range(len(points)):
			line = [points[i], points[(i + 1) % len(points)]]

			move = (line[0] - line[1]).normalize().rotate(-90)

			p = line[1] + move * ball.radius

			if inside(p.x, ball.center.x, line[0].x) and inside(p.y, ball.center.y, line[0].y):
				ball.direction.reflect_ip((line[0] - line[1]).rotate(90))
				self.on_hit(ball, 0, i)
				return True

		for i in range(len(points)):
			if (points[i] - ball.center).length() <= ball.radius:
				ball.direction.reflect_ip(pygame.Vector2(points[i] - ball.center))
				self.on_hit(ball, 1, i)
				return True

		return False


class BlockWithBall(Block):
	def __init__(self, rect: pygame.Rect, color: pygame.Color, sound: str):
		super().__init__(rect, color, sound)
		self.ball_color = self.color - pygame.Color(50, 50, 50, 0)

	@override
	def draw(self, surface: pygame.Surface, glow_surf: pygame.Surface):
		super().draw(surface, glow_surf)
		pygame.draw.circle(surface, self.ball_color, self.rect.center, min(self.rect.height, self.rect.width) * 0.35)

	@override
	def on_hit(self, ball: Ball, side_or_corner: Literal[0] | Literal[1], which: int):
		super().on_hit(ball, side_or_corner, which)
		BallManager().spawn(
			pygame.Vector2(self.rect.center), pygame.Vector2(1, 0).rotate(random.randint(1, 360)), self.ball_color
		)


class BlockDouble(Block):
	def __init__(self, rect: pygame.Rect, color: pygame.Color, sound: str):
		super().__init__(rect, color, sound)
		self.lives: int = 2

	@override
	def draw(self, surface: pygame.Surface, glow_surf: pygame.Surface):
		super().draw(surface, glow_surf)

		if self.lives != 1:
			pygame.draw.rect(surface, "white", self.rect, width=5, border_radius=10)

	@override
	def on_hit(self, ball: Ball, side_or_corner: Literal[0, 1], which: int):
		ball.bounce_anim()
		SoundManager().play(self.sound)

		self.lives -= 1
		if self.lives <= 0:
			self.kill()
