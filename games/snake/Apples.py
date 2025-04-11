import pygame

from .HexCell import HexCell
from .HexBoard import HexBoard
from .Snake import Snake
from .utils import draw_cube

import random


class Apples:
	def __init__(self, board: HexBoard) -> None:
		self.arr: set[HexCell] = set()
		self.board: HexBoard = board

		self.color = ((255, 79, 121), (201, 54, 138), (0, 255, 197))

	def __len__(self) -> int:
		return len(self.arr)

	def draw(self, surface: pygame.Surface) -> None:
		for apple in self.arr:
			center = apple.axial_to_pixel(self.board.cell_size, self.board.offset)
			points = apple.get_polygon_points(center, self.board.cell_size)
			draw_cube(surface, points, center, self.color)

	def add_random_apple(self, snake: Snake) -> None:
		# Calculate available cells: cells on the board not occupied by the snake or an apple.
		occupied = set(snake.arr) | self.arr
		available = set(self.board.cells) - occupied

		if available:
			chosen_cell = random.choice(list(available))
			self.arr.add(chosen_cell)
