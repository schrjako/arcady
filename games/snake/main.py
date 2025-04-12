import pygame

from .hex import HexBoard
from .snake import Snake
from .spawnables import SpawnableManager, Apple, Bomb
from .collisionManager import CollisionManager

import random
from enum import Enum

# The article about hexagonal grids I used: https://www.redblobgames.com/grids/hexagons/

path = "./games/snake"


class SnakeGame:
	"""
	The main game class handling initialization, game loop, and rendering for the snake game.
	"""

	class States(Enum):
		NORMAL = 0
		GAME_OVER = 1

	def __init__(
		self,
		screen: pygame.Surface,
		board_radius: int,
		cell_size: float,
	) -> None:
		"""
		Initializes the SnakeGame by creating the hex board.
		"""
		self.screen: pygame.Surface = screen
		self.clock: pygame.time.Clock = pygame.time.Clock()

		self.backgound: tuple[int, int, int] = (26, 27, 38)

		offset: tuple[int, int] = (
			self.screen.get_width() // 2,
			self.screen.get_height() // 2,
		)
		self.board: HexBoard = HexBoard(board_radius, cell_size, offset)

		self.snake: Snake = Snake((0, 0), 5, self.board)

		self.spawnable_manager: SpawnableManager = SpawnableManager(
			self.board, self.snake
		)

		self.collision_manager: CollisionManager = CollisionManager(
			self.snake, self.spawnable_manager, self.game_over
		)

		self.running: bool = True
		self.state: SnakeGame.States = self.States.NORMAL
		self.game_over_msg = ""

	def game_over(self, message: str) -> None:
		self.state = self.States.GAME_OVER
		self.game_over_msg = message

	def draw_game_over(self, message: str) -> None:
		color = (255, 0, 160)

		# Draw dark overlay
		overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
		overlay.set_alpha(150)
		overlay.fill((0, 0, 0))
		self.screen.blit(overlay, (0, 0))

		# Create fonts
		large_font = pygame.font.Font(path + "/fonts/PressStart2P.ttf", 46)
		small_font = pygame.font.Font(path + "/fonts/PressStart2P.ttf", 20)
		
		# Render the main Game Over message.
		game_over_text = large_font.render("GAME OVER", True, color)
		game_over_rect = game_over_text.get_rect(
			center=(self.screen.get_width() // 2, self.screen.get_height() // 2)
		)
		self.screen.blit(game_over_text, game_over_rect)
		
		# Render the message
		message_text = small_font.render(message, True, color)
		extra_rect = message_text.get_rect(
			center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 60)
		)
		self.screen.blit(message_text, extra_rect)

		# Render the "Press Enter to Continue" text
		message_text = small_font.render("Press Enter to Continue", True, color)
		extra_rect = message_text.get_rect(
			center=(self.screen.get_width() // 2, self.screen.get_height() // 2 - 60)
		)
		self.screen.blit(message_text, extra_rect)
		

	def run(self) -> None:
		"""
		Runs the main game loop, handling events and drawing the board.
		"""
		frame = 0

		while self.running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.running = False

				if self.state == self.States.NORMAL:
					if event.type == pygame.KEYDOWN:
						if event.key == pygame.K_LEFT:
							self.snake.turn_left()
						if event.key == pygame.K_RIGHT:
							self.snake.turn_right()

				if self.state == self.States.GAME_OVER:
					if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
						self.running = False

			if self.state == self.States.NORMAL:
				# Move snake
				if frame % 10 == 0:
					self.snake.move()

				# Spawn apples
				if frame % 120 == 0:
					if random.randint(0, len(self.spawnable_manager.get(Apple))) == 0:
						self.spawnable_manager.spawn_random(Apple)

				# Spawn bombs
				if frame % 120 == 0:
					if random.randint(0, len(self.spawnable_manager.get(Bomb))) == 0:
						self.spawnable_manager.spawn_random(Bomb)

				# Update spawnables
				self.spawnable_manager.update()

				# Handle collisions
				self.collision_manager.handle_collisions()

			# Draw everything
			self.screen.fill(self.backgound)

			self.board.draw(self.screen)
			self.snake.draw(self.screen)
			self.spawnable_manager.draw(self.screen)
			
			if self.state == self.States.GAME_OVER:
				self.draw_game_over(self.game_over_msg)

			pygame.display.flip()
			self.clock.tick(60)
			frame += 1


def run(screen: pygame.Surface):
	SnakeGame(screen, board_radius=10, cell_size=17).run()


if __name__ == "__main__":
	pygame.init()
	screen = pygame.display.set_mode((800, 600))
	run(screen)
