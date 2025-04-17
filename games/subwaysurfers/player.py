import pygame
from collections import deque


class player:
	def __init__(self) -> None:
		self.timer: int = 0

	def update(self) -> None:
		self.timer += 1

	def move(self) -> None:
		pass


	def draw(self, surface: pygame.Surface):
		white=(255,255,255)
		pygame.draw.rect(surface,white,(200,150,100,50))
