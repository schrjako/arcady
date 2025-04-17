import pygame

from .sprite import Sprite

from pathlib import Path


class Metrics(Sprite):
	def __init__(self, rect: pygame.Rect, score_color: pygame.Color, lives_color: pygame.Color, lives: int = 3):
		super().__init__()

		self.score: int = 0
		self.lives: int = 3

		self.score_color = score_color
		self.lives_color = lives_color

		self.rect: pygame.Rect = rect

		self.font = pygame.font.Font(str(Path(__file__).parent / "assets/04B_11.ttf"), 25)

	def draw(self, surface: pygame.Surface, glow_surf: pygame.Surface):
		# Draw score
		text_surface = self.font.render(str(self.score), False, self.score_color)
		text_rect = text_surface.get_rect(center=self.rect.center)
		surface.blit(text_surface, text_rect)

		# Draw lives
		padding = 7
		radius = 10
		for i in range(3):
			for s in [surface, glow_surf] if i < self.lives else [surface]:
				pygame.draw.circle(
					s,
					self.lives_color,
					(self.rect.left + radius + i * (2 * radius + padding), self.rect.center[1]),
					radius,
					width=0 if i < self.lives else 1,
				)
