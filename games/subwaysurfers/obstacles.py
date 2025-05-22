import pygame
from collections import deque
from math import atan2
from .vector import Vector, Vector3D


class Obstacle:
	def __init__(self, v, pos, size, opazovalec, width, height, screen) -> None:
		self.timer: int = 0

		self.v = v
		self.pos = pos
		self.size = size
		self.opazovalec = opazovalec
		self.z = 200
		self.zorni_kot = 100
		self.width = width
		self.height = height
		self.Y = 1

	def update(self) -> None:
		self.timer += 1

	def move(self):
		self.pos.y -= self.v

	def draw(self, surface: pygame.Surface):
		white=(255,255,255)
		polovica_screena=Vector(400, 300)

		'''def draw_line(vogal, smer):
			pygame.draw.line(surface, white, vogal.projekcija(self.Y, polovica_screena).totuple, (smer + vogal).projekcija(self.Y, polovica_screena).totuple, width=3)'''
		def pozicija(tocka):
			v = tocka - self.opazovalec
			z_kot = atan2(v.z, v.y)
			x_kot = atan2(v.x, v.y)
			pozicija = Vector(self.screen.get_width() / 2*((x_kot/self.zorni_kot+1)/2), self.screen.get_height() / 2*((zs_kot/self.zorni_kot+1)/2))
			return pozicija

		def draw_line(vogal, smer):
			
			pygame.draw.line(surface, white, pozicija(vogal).totuple, pozicija(smer + vogal).totuple, width=3)

		pozicija_y = pozicija1(self.z, self.y)
		pozicija_y2 = pozicija1(self.z, self.y2)
		vogal1 = Vector3D(pozicija_y, self.y, 400)
		vogal2 = Vector3D(pozicija_y2, self.y2, 400)
		smer= [Vector3D(100, 0, 0), Vector3D(0, 0.3, 0), Vector3D(0, 0, 100)]
		for i in range(3):
			draw_line(vogal1, smer[i])
		for i in range(3):
			draw_line(vogal2, smer[i])
