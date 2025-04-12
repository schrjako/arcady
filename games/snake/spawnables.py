import pygame

from .hex import HexCell, HexBoard
from .snake import Snake
from .utils import draw_cube, draw_triangle

import random
from abc import ABC, abstractmethod
from enum import Enum


class Spawnable(ABC):
	def __init__(self, position: HexCell):
		self.position: HexCell = position
		self.alive: bool = True

	@abstractmethod
	def draw(self, surface: pygame.Surface, board: HexBoard) -> None:
		pass

	def update(self) -> None:
		pass

	def kill(self) -> None:
		self.alive = False


class SpawnableManager:
	def __init__(self, board: HexBoard, snake: Snake):
		self.board: HexBoard = board
		self.snake: Snake = snake
		self.spawnables: dict[type[Spawnable], list[Spawnable]] = {}

	def get_occupied_cells(self) -> set:
		occupied = set(self.snake.body)

		for lst in self.spawnables.values():
			for spawnable in lst:
				occupied.add(spawnable.position)

		return occupied

	def get(self, cls: type[Spawnable]) -> list[Spawnable]:
		return self.spawnables.get(cls, [])

	def spawn_random(self, spawnable_cls: type[Spawnable], *args, **kwargs) -> None:
		"""Spawn a new spawnable of type spawnable_cls at a random free cell."""
		free_cells = set(self.board.cells) - self.get_occupied_cells()
		if free_cells:
			chosen_cell = random.choice(list(free_cells))

			# Instantiate the spawnable with the chosen cell and any additional arguments:
			new_spawnable = spawnable_cls(chosen_cell, *args, **kwargs)

			# Add to spawnables dict
			self.spawnables.setdefault(
				spawnable_cls, []
			)  # Set to empty list if the class is not yet in spawnables
			self.spawnables[spawnable_cls].append(new_spawnable)

	def draw(self, surface: pygame.Surface):
		for lst in self.spawnables.values():
			for spawnable in lst:
				spawnable.draw(surface, self.board)

	def update(self):
		self.spawnables = {
			cls: [s for s in lst if s.update() or s.alive]
			for cls, lst in self.spawnables.items()
		}


class Apple(Spawnable):
	def __init__(self, position: HexCell) -> None:
		super().__init__(position)
		self.color = ((255, 79, 121), (201, 54, 138), (0, 255, 197))

	def draw(self, surface, board):
		center = self.position.get_center(board.cell_size, board.offset)
		points = self.position.get_polygon_points(center, board.cell_size)
		draw_cube(surface, points, center, self.color)


class Bomb(Spawnable):
	class States(Enum):
		BOMB = 0
		WARNING = 1

	def __init__(
		self,
		position,
		pending_duration: int = 180,
		bomb_duration: int = 380,
	):
		"""
		Initialize the bomb.
		  - pending_duration: time (in frames) that the bomb remains in its deactivatable state.
		  - bomb_duration: time (in frames) that the bomb remains armed.
		"""
		super().__init__(position)
		self.pending_duration = pending_duration
		self.bomb_duration = bomb_duration
		self.timer = 0

		self.state: Bomb.States = Bomb.States.WARNING

		self.warning_color = (255, 76, 16)
		self.bomb_color = ((255, 87, 51), (199, 0, 57), (255, 141, 26))

	def update(self):
		self.timer += 1
		if self.state == Bomb.States.WARNING and self.timer >= self.pending_duration:
			# Transition to the bomb state
			self.state = Bomb.States.BOMB
			self.timer = 0  # Reset timer for bomb state duration
		elif self.state == Bomb.States.BOMB and self.timer >= self.bomb_duration:
			# Bomb disappears after being armed for a while
			self.kill()

	def draw(self, surface, board):
		"""
		Draw the bomb. When pending it uses a triangle; when armed a cube.
		"""
		center = self.position.get_center(board.cell_size, board.offset)

		if self.state == Bomb.States.WARNING:
			# Draw as a triangle while deactivatable
			draw_triangle(surface, center, board.cell_size * 0.6, self.warning_color)
		elif self.state == Bomb.States.BOMB:
			# Draw as a cube when armed
			points = self.position.get_polygon_points(center, board.cell_size)
			draw_cube(surface, points, center, self.bomb_color)
