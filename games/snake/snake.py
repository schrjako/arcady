import pygame

from .hex import HexCell, HexBoard
from . import utils

from collections import deque


class Snake:
	def __init__(self, location: tuple[int, int], length: int, board: HexBoard) -> None:
		self.board = board

		self.direction: int = 0
		self.length: int = length

		self.body: deque[HexCell] = deque()
		self.body.append(HexCell(location[0], location[1]))

		# Color constants
		self.head_color = ((194, 120, 87), (166, 61, 64), (255, 206, 75))
		self.part_color = ((126, 132, 163), (92, 97, 122), (165, 173, 203))

	def turn_right(self) -> None:
		self.direction = (self.direction - 1) % 6

	def turn_left(self) -> None:
		self.direction = (self.direction + 1) % 6

	def head(self) -> HexCell:
		return self.body[0]

	def move(self) -> None:
		while len(self.body) >= self.length:
			self.body.pop()

		new_head = self.board.get_neighbour(self.body[0], self.direction)
		self.body.appendleft(new_head)

	def grow(self) -> None:
		self.length += 1

	def draw(self, surface: pygame.Surface):
		for index, part in enumerate(self.body):
			center = part.get_center(self.board.cell_size, self.board.offset)
			points = part.get_polygon_points(center, self.board.cell_size)
			utils.draw_cube(
				surface,
				points,
				center,
				self.head_color if index == 0 else self.part_color,
			)
