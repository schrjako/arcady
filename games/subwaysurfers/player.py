import pygame
from collections import deque

from .vector import Vector, Vector3D


class Player:
	def __init__(self, x, y, width, height, g, a, screen) -> None:
		self.timer: int = 0
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.g = g           #g je pospešek navzdol
		self.vy = 0
		self.jumps = 0
		self.vright = 0
		self.vleft = 0
		self.a = a          #a je pospešek levo in desno
		self.screen_size = screen

		self.y_odcrte=0.5
		self.y_odcrte2= 0.8
		self.visina_kvadra=100
		self.sirina_kvadra=200
		self.Y=1

	def update(self) -> None:
		self.timer += 1

	def jump(self) -> None:
		self.vy = self.vy - self.g
		self.y = self.y - self.vy
		if self.y > 400:
			self.y = 400
			self.jumps = 0

	def move(self):
		if self.vright != 0:
			self.vright = self.vright - self.a
			self.x = self.x + self.vright
		if self.vleft != 0:
			self.vleft = self.vleft - self.a
			self.x = self.x - self.vleft 

	def draw(self, surface: pygame.Surface):
		white=(255,255,255)
		pygame.draw.rect(surface,white,(self.x, self.y, self.width, self.height))
