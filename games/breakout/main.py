import pygame

from .ball import BallManager
from .paddle import Paddle
from .block import Block, BlockWithBall
from .metrics import Metrics
from .utils import glow, limit
from .particle import Particle, ParticleManager
from .sound import SoundManager

import random
from typing import Literal
from pathlib import Path


class Colors:
	def __init__(self):
		self.background = pygame.Color(5, 5, 15)
		self.paddle = pygame.Color(0, 255, 255)
		self.ball = pygame.Color(0, 191, 255)
		self.block = {
			"normal": [
				pygame.Color(255, 140, 160),  # lively pastel red
				pygame.Color(255, 190, 140),  # lively pastel orange
				pygame.Color(255, 250, 140),  # lively pastel yellow
				pygame.Color(140, 255, 170),  # lively pastel green
				pygame.Color(150, 200, 255),  # lively pastel blue
				pygame.Color(170, 140, 255),  # lively pastel indigo
				pygame.Color(255, 140, 255),  # lively pastel violet
			]
		}
		self.lives = pygame.Color(255, 100, 120)
		self.text = pygame.Color(200, 255, 255)


class Breakout:
	def __init__(self, screen: pygame.Surface):
		self.screen: pygame.Surface = screen
		self.menu_size = self.screen.get_size()
		self.resize_screen((700, 650))

		self.glow_surf: pygame.Surface = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
		self.draw_surf: pygame.Surface = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)

		self.clock: pygame.time.Clock = pygame.time.Clock()
		self.running: bool = True

		self.state: Literal["playing", "serving", "gameover"]

		self.colors = Colors()

		self.draw_surf.set_colorkey(self.colors.background)

		self.fonts: dict[str, pygame.font.Font] = {
			"large": pygame.font.Font(str(Path(__file__).parent / "assets/04B_03.ttf"), 40),
			"smaller": pygame.font.Font(str(Path(__file__).parent / "assets/04B_03.ttf"), 28),
		}

		self.metrics: Metrics = Metrics(
			pygame.Rect(35, 5, self.screen.get_width() - 35 * 2, 60), self.colors.text, self.colors.lives
		)

		self.paddle: Paddle = Paddle(
			self.screen.get_width(),
			self.screen.get_height() - 60,
			width=100,
			height=15,
			speed=8,
			color=self.colors.paddle,
		)
		self.blocks: list[Block]

		self.new_level()
		self.serve()

	def resize_screen(self, dimensions: tuple[int, int]):
		self.screen = pygame.display.set_mode(dimensions)

	def new_level(self):
		self.spawn_blocks(rows=6, columns=8, start_y=self.metrics.rect.bottom, width=75, height=35, padding=5)

	def serve(self):
		"""
		Reset paddle position, create new ball and spawn blocks. Also set state to serving
		"""
		self.state = "serving"

		self.paddle.position.x = self.screen.get_width() / 2

		BallManager().balls = []  # Better safe than sorry
		BallManager().spawn(
			self.paddle.position - pygame.Vector2(0, 20),
			pygame.Vector2(0, -1).rotate(random.randint(-30, 30)),
			self.colors.ball,
		)

	def spawn_blocks(self, rows: int, columns: int, start_y: float, width: float, height: float, padding: float):
		self.blocks = []

		start_x = (self.screen.get_width() - width * columns - padding * (columns - 1)) / 2

		for i in range(rows):
			for j in range(columns):
				type = BlockWithBall if random.randint(0, 17) == 0 else Block
				self.blocks.append(
					type(
						pygame.Rect(
							start_x + j * (width + padding),
							start_y + i * (height + padding),
							width,
							height,
						),
						color=self.colors.block["normal"][i],
						sound=f"block_hit_{rows - i}",
					)
				)

	def draw_game_over(self, surface: pygame.Surface):
		screen_width, screen_height = surface.get_size()
		overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
		overlay.fill((0, 0, 0, 180))  # semi-transparent dark overlay
		surface.blit(overlay, (0, 0))

		# Draw game over box
		box_width, box_height = 300, 220
		box_rect = pygame.Rect(
			(screen_width - box_width) // 2, (screen_height - box_height) // 2, box_width, box_height
		)
		pygame.draw.rect(surface, (51, 0, 67), box_rect, width=0)
		pygame.draw.rect(surface, (255, 255, 255), box_rect, width=2)

		# GAME OVER text
		text_surface = self.fonts["smaller"].render("GAME OVER", True, self.colors.text)
		text_rect = text_surface.get_rect(center=(screen_width // 2, box_rect.top + 40))
		surface.blit(text_surface, text_rect)

		# SCORE
		score_text = self.fonts["smaller"].render("SCORE", True, self.colors.text)
		score_val = self.fonts["smaller"].render(f"{self.metrics.score:05d}", True, self.colors.text)
		surface.blit(score_text, (box_rect.left + 30, box_rect.top + 90))
		surface.blit(score_val, (box_rect.left + 30, box_rect.top + 120))

		# ENTER text
		button_rect = pygame.Rect(box_rect.left + 20, box_rect.bottom - 60, box_rect.width - 40, 40)
		pygame.draw.rect(surface, (255, 255, 255), button_rect, width=2)

		play_again_text = self.fonts["smaller"].render("PRESS ENTER", True, self.colors.text)
		play_again_rect = play_again_text.get_rect(center=button_rect.center)
		surface.blit(play_again_text, play_again_rect)

	def run(self):
		while self.running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.running = False

				if event.type == pygame.KEYDOWN:
					if self.state == "serving" and (event.key in [pygame.K_SPACE, pygame.K_RETURN, pygame.K_UP]):
						self.state = "playing"

					if self.state == "gameover" and event.key == pygame.K_RETURN:
						self.running = False

			self.screen.fill(self.colors.background)
			self.draw_surf.fill((0, 0, 0, 0))
			self.glow_surf.fill((0, 0, 0, 0))

			if self.state == "serving":
				text_surface = self.fonts["large"].render("Press space to start", False, self.colors.text)
				text_rect = text_surface.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() - 250))
				self.screen.blit(text_surface, text_rect)

			elif self.state == "playing":
				keys = pygame.key.get_pressed()
				if keys[pygame.K_LEFT]:
					self.paddle.move(-1)
				if keys[pygame.K_RIGHT]:
					self.paddle.move(1)

				# Update balls' position based on velocity and remove dead
				BallManager().update()

				for ball in BallManager().balls:
					# Bounce from walls
					bounced = False

					if ball.center.x <= ball.radius or ball.center.x >= self.screen.get_width() - ball.radius:
						ball.direction.x *= -1
						bounced = True

					ball.center.x = limit(ball.center.x, ball.radius, self.screen.get_width() - ball.radius)

					if ball.center.y <= ball.radius:
						ball.direction.y *= -1
						bounced = True

					ball.center.y = max(ball.center.y, ball.radius)

					if bounced:
						ball.bounce_anim()
						SoundManager().play("wall_hit")

						def draw_glow(particle: Particle, surface: pygame.Surface, glow_surf: pygame.Surface):
							pygame.draw.circle(glow_surf, particle.data["color"], particle.data["position"], 20)

						ParticleManager().spawn(
							10, draw_glow, [], data={"position": ball.center.copy(), "color": ball.color}
						)

					# Bounce from paddle
					self.paddle.bounce(ball)

					# Bounce from blocks
					for b in self.blocks:
						if b.bounce(ball):
							self.metrics.score += 1
							b.kill()

					# Check if the ball fell out of the screen
					if ball.center.y >= self.screen.get_height() - ball.radius:
						ball.kill()

				# Check for lose
				if len(BallManager().balls) == 0:
					self.metrics.lives -= 1

					if self.metrics.lives <= 0:
						self.state = "gameover"
					else:
						self.serve()

				# Remove all dead blocks
				self.blocks = [b for b in self.blocks if b.is_alive()]

				# Check for win
				if len(self.blocks) == 0:
					self.new_level()

			# Update particles (must outside of "playing" so particles don't get stuck)
			ParticleManager().update()

			# Draw
			# =======================================================

			self.metrics.draw(self.draw_surf, self.glow_surf)
			self.paddle.draw(self.draw_surf, self.glow_surf)
			BallManager().draw(self.draw_surf, self.glow_surf)
			for b in self.blocks:
				b.draw(self.draw_surf, self.glow_surf)

			if self.state == "gameover":
				self.draw_game_over(self.draw_surf)

			ParticleManager().draw(self.draw_surf, self.glow_surf)

			self.screen.blit(glow(self.glow_surf, falloff=10, quality=0.5), (0, 0), special_flags=pygame.BLEND_RGB_ADD)

			self.screen.blit(self.draw_surf, (0, 0))

			pygame.display.flip()
			self.clock.tick(60)

		self.resize_screen(self.menu_size)


def run(screen: pygame.Surface):
	Breakout(screen).run()
