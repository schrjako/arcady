import pygame

from .sprite import Sprite
from .ball import Ball
from .sound import SoundManager

from typing import Literal


class Paddle(Sprite):
	def __init__(
		self,
		screen_width: int,
		y: float,
		width: float,
		height: float,
		speed: float,
		acc: float,
		resistance: float,
		color: pygame.Color,
	):
		super().__init__()

		self.screen_width = screen_width

		self.max_speed: float = speed
		self.acc: float = acc
		self.resistance: float = resistance
		self.velocity = 0

		self.position: pygame.Vector2 = pygame.Vector2(screen_width / 2, y)
		self.width = width
		self.height = height

		self.color = color

	def get_rect(self) -> pygame.Rect:
		return pygame.Rect(self.position.x - self.width / 2, self.position.y, self.width, self.height)

	def draw(self, surface: pygame.Surface, glow_surf: pygame.Surface):
		for s in [surface, glow_surf]:
			pygame.draw.rect(
				s,
				self.color,
				self.get_rect() if s == surface else self.get_rect().move(0, -10),
				border_radius=int(self.height * 0.8),
				border_top_left_radius=0,
				border_top_right_radius=0,
			)

	def update(self):
		self.position += pygame.Vector2(self.velocity, 0)
		self.position.x = max(min(self.position.x, self.screen_width - self.width / 2), self.width / 2)
		self.velocity *= self.resistance

	def move(self, dir: Literal[-1, 1]):
		"""
		Parameters:
		dir: The direction to move the paddle; 1 to right, -1 to left.
		"""
		self.velocity += self.acc * dir

	def bounce(self, ball: Ball):
		if (
			abs(ball.center.y - self.position.y) <= ball.radius / 2
			and abs(ball.center.x - self.position.x) <= self.width / 2 + ball.radius
		):
			angle = (ball.center.x - self.position.x) / self.width * 2 * 60
			ball.direction = pygame.Vector2(0, -1).rotate(angle)
			ball.center.y = self.position.y - ball.radius  # Pop it out of the paddle to insure no clipping
			ball.bounce_anim()
			SoundManager().play("paddle_hit")
