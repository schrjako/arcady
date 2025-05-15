import pygame

from abc import abstractmethod, ABC


class Sprite(ABC):
	def __init__(self):
		self.alive = True

	@abstractmethod
	def draw(self, surface: pygame.Surface, glow_surf: pygame.Surface) -> None:
		pass

	def kill(self):
		self.alive = False

	def is_alive(self) -> bool:
		return self.alive
