import pygame

from .sprite import Sprite

from pathlib import Path
import base64
import binascii


class Metrics(Sprite):
	def __init__(self, rect: pygame.Rect, score_color: pygame.Color, lives_color: pygame.Color, lives: int = 3):
		super().__init__()

		self.score: int = 0
		self.lives: int = 3

		self.score_color = score_color
		self.lives_color = lives_color

		self.rect: pygame.Rect = rect

		self.font = pygame.font.Font(str(Path(__file__).parent / "assets" / "04B_11.ttf"), 25)

		self.file = Path(__file__).parent / "assets" / ".SCORES_breakout"

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

	def save(self):
		self.file.parent.mkdir(parents=True, exist_ok=True)
		encoded = base64.b64encode(str(self.score).encode("utf-8")).decode("ascii")
		with self.file.open("a", encoding="utf-8") as fout:
			fout.write(f"{encoded}\n")

	def best_score(self):
		if not self.file.exists():
			return None

		with self.file.open("r", encoding="utf-8") as fin:
			try:
				decoded_scores = [int(base64.b64decode(line.strip()).decode("utf-8")) for line in fin if line.strip()]
			except (ValueError, binascii.Error):
				raise ValueError("Invalid encoded data in metrics file")

		if not decoded_scores:
			return None

		return max(decoded_scores)
