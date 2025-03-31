import pygame
import math
import random
from collections import deque

# The article about hexagonal grids I used: https://www.redblobgames.com/grids/hexagons/

DEBUG = False


def draw_cube(
	surface: pygame.Surface,
	points: list[tuple[float, float]],
	center: tuple[float, float],
	colors: (
		tuple[pygame.Color, pygame.Color, pygame.Color]
		| tuple[tuple[int, int, int], tuple[int, int, int], tuple[int, int, int]]
	),
):
	pygame.draw.polygon(surface, colors[0], points[:3] + [center])
	pygame.draw.polygon(surface, colors[1], points[2:5] + [center])
	pygame.draw.polygon(surface, colors[2], points[4:6] + [points[0], center])


class HexCell:
	"""
	Represents a single hexagonal cell on the board using axial coordinates.
	"""

	def __init__(self, q: int, r: int) -> None:
		"""
		Initializes the HexCell with axial coordinates and size.
		"""
		self.q: int = q
		self.r: int = r

	def s(self):
		return -(self.q + self.r)

	def __eq__(self, other) -> bool:
		return self.q == other.q and self.r == other.r

	def __hash__(self) -> int:
		return (self.q, self.r).__hash__()

	def __add__(self, other):
		return HexCell(self.q + other.q, self.r + other.r)

	def __sub__(self, other):
		return HexCell(self.q - other.q, self.r - other.r)

	def __mul__(self, scalar: int):
		return HexCell(self.q * scalar, self.r * scalar)

	def __str__(self):
		return f"[{self.q}, {self.r}, {self.s()}]"

	def distance_to(self, other) -> int:
		vec = self - other
		return max(abs(vec.q), abs(vec.r), abs(vec.s()))

	def axial_to_pixel(
		self, size: float, offset: tuple[int, int]
	) -> tuple[float, float]:
		"""
		Converts axial coordinates (q, r) to pixel coordinates for drawing.
		"""
		x: float = size * (math.sqrt(3) * self.q + math.sqrt(3) / 2 * self.r)
		y: float = size * (3 / 2 * self.r)
		return (x + offset[0], y + offset[1])

	def get_polygon_points(
		self, center: tuple[float, float], size: float
	) -> list[tuple[float, float]]:
		"""
		Calculates the vertices of the hexagon based on its center.
		"""
		points: list[tuple[float, float]] = []

		for i in range(6):
			angle_deg: float = 60 * i - 30  # Adjust for a pointy-topped orientation.
			angle_rad: float = math.radians(angle_deg)
			x: float = center[0] + size * math.cos(angle_rad)
			y: float = center[1] + size * math.sin(angle_rad)
			points.append((x, y))

		return points


class HexBoard:
	"""
	Represents a hexagonal board made up of HexCell objects.
	"""

	def __init__(self, radius: int, cell_size: float, offset: tuple[int, int]) -> None:
		"""
		Initializes the hex board by generating its cells.
		"""
		self.radius: int = radius
		self.cell_size: float = cell_size
		self.offset: tuple[int, int] = offset
		self.cells: list[HexCell] = []
		self.generate_board()

	def generate_board(self) -> None:
		"""
		Generates a hexagon-shaped board using axial coordinates.

		The board will include cells where the coordinates satisfy:
		-radius <= q <= radius
		-radius <= r <= radius
		-radius <= -(q + r) <= radius
		"""
		N: int = self.radius
		for q in range(-N, N + 1):
			for r in range(-N, N + 1):
				if -N <= -q - r <= N:
					self.cells.append(HexCell(q, r))

	def get_neighbour(self, cell: HexCell, direction: int) -> HexCell:
		"""
		Returns the axial coordinates of the neighboring hex cell in the given direction,
		with wrapping at the board edges.
		"""
		directions: list[HexCell] = [
			HexCell(i[0], i[1])
			for i in [
				(1, 0),  # 0
				(1, -1),  # 1
				(0, -1),  # 2
				(-1, 0),  # 3
				(-1, 1),  # 4
				(0, 1),  # 5
			]
		]

		if direction < 0 or direction >= len(directions):
			raise ValueError("Direction must be between 0 and 5.")

		candidate: HexCell = cell + directions[direction]
		N: int = self.radius

		# Check if it is in the boundaries and return if so
		if candidate.distance_to(HexCell(0, 0)) <= N:
			return candidate

		# print(
		# 	f"out: candidate: {candidate}, distance to center: {candidate.distance_to(HexCell(0, 0))}"
		# )

		# Loop trough other centers
		construct = [N, N + 1, -(2 * N + 1)]
		for i in range(3):
			for j in [1, -1]:
				center = HexCell(construct[i], construct[(i + 1) % 3]) * j
				# print(f"  dist to {center}: {candidate.distance_to(center)}")
				if candidate.distance_to(center) <= N:
					return candidate - center

		raise RuntimeError(
			"This shouldn't happen (cell not in the range of any neighbour center)"
		)

	def draw(self, surface: pygame.Surface) -> None:
		"""
		Draws all hex cells onto the given pygame surface.
		"""
		if DEBUG:
			font = pygame.font.SysFont(None, 24)

		for cell in self.cells:
			center = cell.axial_to_pixel(self.cell_size, self.offset)
			points = cell.get_polygon_points(center, self.cell_size)
			pygame.draw.polygon(surface, (200, 200, 200), points, 2)

			if DEBUG:
				text = font.render(f"{cell.q},{cell.r}", True, (255, 255, 255))
				text_rect = text.get_rect(center=center)
				surface.blit(text, text_rect)


class Snake:
	def __init__(self, location: tuple[int, int], length: int, board: HexBoard) -> None:
		self.board = board

		self.direction: int = 0
		self.length: int = length

		self.arr: deque[HexCell] = deque()
		self.arr.append(HexCell(location[0], location[1]))

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
		for i in self.arr:
			center = i.axial_to_pixel(self.board.cell_size, self.board.offset)
			points = i.get_polygon_points(center, self.board.cell_size)
			draw_cube(
				surface,
				points,
				center,
				((146, 148, 149), (66, 63, 63), (132, 134, 134)),
			)


class Apples:
	def __init__(self, board: HexBoard) -> None:
		self.arr: set[HexCell] = set()
		self.board: HexBoard = board

	def __len__(self) -> int:
		return len(self.arr)

	def draw(self, surface: pygame.Surface) -> None:
		for apple in self.arr:
			center = apple.axial_to_pixel(self.board.cell_size, self.board.offset)
			points = apple.get_polygon_points(center, self.board.cell_size)
			draw_cube(surface, points, center, ((250, 0, 0), (132, 8, 4), (0, 147, 0)))

	def add_random_apple(self, snake: Snake) -> None:
		# Calculate available cells: cells on the board not occupied by the snake or an apple.
		occupied = set(snake.arr) | self.arr
		available = set(self.board.cells) - occupied

		if available:
			chosen_cell = random.choice(list(available))
			self.arr.add(chosen_cell)


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

		self.offset: tuple[int, int] = (self.screen.get_width() // 2, self.screen.get_height() // 2)

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

			self.screen.fill((30, 30, 30))

			self.board.draw(self.screen)
			self.snake.draw(self.screen)
			self.apples.draw(self.screen)

			pygame.display.flip()
			self.clock.tick(60)
			frame += 1

def run(screen: pygame.Surface):
	SnakeGame(screen, board_radius=6, cell_size=20).run()

if __name__ == "__main__":
	pygame.init()
	screen = pygame.display.set_mode((800, 600))
	run(screen)