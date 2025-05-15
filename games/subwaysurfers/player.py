import pygame
from collections import deque


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

		polovica_screena=400
		polovica_screena_z=300
		
		def narisi_crto(y, y2, x, z, x2, z2):
			x = (1-y/self.Y)*x + (y/self.Y)*(polovica_screena)
			z = (1-y/self.Y)*z + (y/self.Y)*(polovica_screena_z)
			x2 = (1-y2/self.Y)*x2 + (y2/self.Y)*(polovica_screena)
			z2 = (1-y2/self.Y)*z2 + (y2/self.Y)*(polovica_screena_z)
			pygame.draw.line(surface, white, [x, z], [x2, z2], width=3)

		'''zaceten_x=500
		zaceten_z=500
		x = (1-self.y_odcrte/self.Y)*zaceten_x + (self.y_odcrte/self.Y)*(polovica_screena)
		z = (1-self.y_odcrte/self.Y)*zaceten_z + (self.y_odcrte/self.Y)*(polovica_screena_z)
		pygame.draw.line(surface, white, [400, 400], [400 + x, 400 + z], width=3)
		pygame.draw.line(surface, white, [400 + x, 400], [400 + x + x, 400 + z], width=3)'''
		narisi_crto(self.y_odcrte, 500, 400, 500, 500)
		narisi_crto(self.y_odcrte, 500, 400, 600, 400)
		narisi_crto(self.y_odcrte, 500, 500, 600, 500)
		narisi_crto(self.y_odcrte, 600, 400, 600, 500)

		narisi_crto(self.y_odcrte2, 500, 400, 500, 500)
		narisi_crto(self.y_odcrte2, 500, 400, 600, 400)
		narisi_crto(self.y_odcrte2, 500, 500, 600, 500)
		narisi_crto(self.y_odcrte2, 600, 400, 600, 500)

