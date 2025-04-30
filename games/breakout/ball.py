import pygame

from .sprite import Sprite
from .utils import no_null, limit

import math


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

	def bounce(self) -> None:
		self.impulse_stretch(self.speed * -0.03)

	def update(self) -> None:
		# 1. Move
		self.center += self.direction * self.speed

		# 2. Compute speed-based desired target
		speed_target = 1.0 + self.speed * self._MOVE_STRETCH
		speed_target = limit(speed_target, self._MIN_STRETCH, self._MAX_STRETCH)

		# 3. Slowly adjust actual stretch target (← delayed response!)
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
		pygame.draw.line(glow_surf, self.color, self.center, self.center - self.direction * self.speed * 7, width=7)
