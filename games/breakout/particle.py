from __future__ import annotations

import pygame

from .sprite import Sprite
from .utils import singleton

from typing import Any, Protocol, Sequence
from abc import abstractmethod


# Define a protocol for the draw function
class DrawFunc(Protocol):
	def __call__(self, particle: Particle, surface: pygame.Surface, glow_surf: pygame.Surface) -> None: ...


@singleton
class ParticleManager:
	def __init__(self) -> None:
		self.particles: list[Particle] = []

	def spawn(self, lifespan: int, draw_func: DrawFunc, effects: Sequence[Effect], data: dict[str, Any] = {}) -> None:
		self.particles.append(Particle(lifespan, draw_func, effects))
		self.particles[-1].data = data
		for e in self.particles[-1].effects:
			e.init(self.particles[-1])

	def update(self) -> None:
		for particle in self.particles:
			particle.update()
		self.particles = [p for p in self.particles if p.is_alive()]

	def draw(self, surface: pygame.Surface, glow_surf: pygame.Surface) -> None:
		for particle in self.particles:
			particle.draw(surface, glow_surf)


class Particle(Sprite):
	def __init__(self, lifespan: int, draw_func: DrawFunc, effects: Sequence[Effect]) -> None:
		super().__init__()
		self.lifespan = lifespan
		self.time = 0
		self._draw = draw_func
		self.effects = effects

		self.data: dict[str, Any]

	def update(self) -> None:
		self.time += 1
		if self.time >= self.lifespan:
			self.kill()
			return
		for effect in self.effects:
			effect.update(self)

	def draw(self, surface: pygame.Surface, glow_surf: pygame.Surface) -> None:
		self._draw(self, surface, glow_surf)


class Effect:
	def __init__(self):
		pass

	@abstractmethod
	def init(self, particle: Particle):
		"""Initialise particle data."""
		...

	@abstractmethod
	def update(self, particle: Particle): ...
