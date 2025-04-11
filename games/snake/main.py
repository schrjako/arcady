import pygame

from .HexBoard import HexBoard
from .Snake import Snake
from .Apples import Apples

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

		self.offset: tuple[int, int] = (
			self.screen.get_width() // 2,
			self.screen.get_height() // 2,
		)

		# Background color
		self.backgound: tuple[int, int, int] = (26, 27, 38)

		self.board: HexBoard = HexBoard(board_radius, cell_size, self.offset)
		self.snake: Snake = Snake((0, 0), 5, self.board)
		self.apples: Apples = Apples(self.board)

		self.running: bool = True

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

			# Eat apples
			if self.snake.head() in self.apples.arr:
				self.snake.length += 1
				self.apples.arr.remove(self.snake.head())

			# Spawn apples
			if frame % 120 == 0 and len(self.apples) < 5:
				if random.randint(0, len(self.apples)) == 0:
					self.apples.add_random_apple(self.snake)

			# Check for self collision (game over)
			if self.snake.head() in list(self.snake.arr)[1:]:
				self.running = False

			self.screen.fill(self.backgound)

			self.board.draw(self.screen)
			self.snake.draw(self.screen)
			self.apples.draw(self.screen)

			pygame.display.flip()
			self.clock.tick(60)
			frame += 1


def run(screen: pygame.Surface):
	SnakeGame(screen, board_radius=10, cell_size=17).run()


if __name__ == "__main__":
	pygame.init()
	screen = pygame.display.set_mode((800, 600))
	run(screen)
