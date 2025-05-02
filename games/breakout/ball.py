import pygame

from .sprite import Sprite
from .utils import no_null, limit, singleton

import math


@singleton
class BallManager:
	def __init__(self):
		self.balls: list[Ball] = []
		self.ball_radius: float = 10
		self.ball_speed: float = 6

	def spawn(self, position: pygame.Vector2, direction: pygame.Vector2, color: pygame.Color):
		self.balls.append(Ball(self.ball_radius, position, direction, self.ball_speed, color))

	def update(self):
		for ball in self.balls:
			ball.update()
		self.balls = [b for b in self.balls if b.is_alive()]

	def draw(self, surface: pygame.Surface, glow_surf: pygame.Surface) -> None:
		for ball in self.balls:
			ball.draw(surface, glow_surf)


class Ball(Sprite):
	def __init__(
		self, radius: float, position: pygame.Vector2, direction: pygame.Vector2, speed: float, color: pygame.Color
	):
		super().__init__()
		self.direction = direction
		self.speed = speed
		self.center = position
		self.radius = radius
		self.color = color

		# squash/stretch state
		self.stretch: float = 1.0
		self.stretch_vel: float = 0.0
		self.stretch_target: float = 1.0

		# physics constants
		self._SPRING_K: float = 0.9  # ← stiffer spring = more wobble
		self._DAMPING: float = 0.12  # ← less damping = longer oscillation
		self._MOVE_STRETCH: float = 0.015
		self._TARGET_DECAY: float = 0.01  # ← how fast target returns to 1.0

		self._MIN_STRETCH: float = 0.5
		self._MAX_STRETCH: float = 2.2

	def impulse_stretch(self, impulse: float) -> None:
		self.stretch_vel += impulse

	def bounce_anim(self) -> None:
		self.impulse_stretch(self.speed * -0.03)

	def update(self) -> None:
		# 1. Move
		self.center += self.direction * self.speed

		# 1.5 Adjust direction to avoid getting stuck if too horizontal
		def sign(a: float):
			return 1 if a >= 0 else -1

		adjust: float = 0
		threshold: float = math.cos(math.radians(10))
		if abs(self.direction.x) > threshold:
			adjust = 0.5 * sign(self.direction.x) * sign(self.direction.y)

		self.direction.rotate_ip(adjust)

		# 2. Compute speed-based desired target
		speed_target = 1.0 + self.speed * self._MOVE_STRETCH
		speed_target = limit(speed_target, self._MIN_STRETCH, self._MAX_STRETCH)

		# 3. Slowly adjust actual stretch target
		self.stretch_target += (speed_target - self.stretch_target) * self._TARGET_DECAY

		# 4. Spring toward target
		spring_force: float = self._SPRING_K * (self.stretch_target - self.stretch)
		self.stretch_vel += spring_force

		# 5. Damping
		self.stretch_vel *= math.exp(-self._DAMPING)

		# 6. Integrate
		self.stretch += self.stretch_vel
		self.stretch = limit(self.stretch, self._MIN_STRETCH, self._MAX_STRETCH)

	def draw(self, surface: pygame.Surface, glow_surf: pygame.Surface) -> None:
		for s in [surface, glow_surf]:
			ball_surf = pygame.Surface(
				(no_null(2 * self.radius * self.stretch), no_null(2 * self.radius / self.stretch)),
				flags=pygame.SRCALPHA,
			)
			ball_surf.fill((0, 0, 0, 0))
			pygame.draw.ellipse(ball_surf, self.color, ball_surf.get_rect())
			ball_surf = pygame.transform.rotate(ball_surf, self.direction.angle_to((1, 0)))

			s.blit(ball_surf, self.center - (self.radius, self.radius))

		# Tail
		pygame.draw.line(glow_surf, self.color, self.center, self.center - self.direction * self.speed * 8, width=8)
