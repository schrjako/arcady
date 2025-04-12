import pygame

from .hex import HexBoard
from .snake import Snake
from .spawnables import SpawnableManager, Apple, Bomb
from .collisionManager import CollisionManager

import random

# The article about hexagonal grids I used: https://www.redblobgames.com/grids/hexagons/


class SnakeGame:
	"""
	The main game class handling initialization, game loop, and rendering for the snake game.
	"""

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

	def game_over(self, message: str) -> None:
		self.running = False

	def run(self) -> None:
		"""
		Runs the main game loop, handling events and drawing the board.
		"""
		frame = 0

		while self.running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.running = False
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_LEFT:
						self.snake.turn_left()
					if event.key == pygame.K_RIGHT:
						self.snake.turn_right()

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

			pygame.display.flip()
			self.clock.tick(60)
			frame += 1


def run(screen: pygame.Surface):
	SnakeGame(screen, board_radius=10, cell_size=17).run()


if __name__ == "__main__":
	pygame.init()
	screen = pygame.display.set_mode((800, 600))
	run(screen)
