import pygame

from .HexCell import HexCell
from .HexBoard import HexBoard
from . import utils

from collections import deque


class Snake:
	def __init__(self, location: tuple[int, int], length: int, board: HexBoard) -> None:
		self.board = board

		self.direction: int = 0
		self.length: int = length

		self.arr: deque[HexCell] = deque()
		self.arr.append(HexCell(location[0], location[1]))

		# Color constants
		self.head_color = ((194, 120, 87), (166, 61, 64), (255, 206, 75))
		self.part_color = ((126, 132, 163), (92, 97, 122), (165, 173, 203))

	def turn_right(self) -> None:
		self.direction = (self.direction - 1) % 6

	def turn_left(self) -> None:
		self.direction = (self.direction + 1) % 6

	def head(self) -> HexCell:
		return self.arr[0]

	def move(self) -> None:
		while len(self.arr) >= self.length:
			self.arr.pop()

		new_head = self.board.get_neighbour(self.arr[0], self.direction)
		self.arr.appendleft(new_head)

	def draw(self, surface: pygame.Surface):
		for index, part in enumerate(self.arr):
			center = part.axial_to_pixel(self.board.cell_size, self.board.offset)
			points = part.get_polygon_points(center, self.board.cell_size)
			utils.draw_cube(
				surface,
				points,
				center,
				self.head_color if index == 0 else self.part_color,
			)
