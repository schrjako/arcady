import math


class Point:
	def __init__(self, x: float, y: float):
		self.x = x
		self.y = y

	def __add__(self, other: "Point"):
		return Point(self.x + other.x, self.y + other.y)

	def __sub__(self, other: "Point"):
		return Point(self.x - other.x, self.y - other.y)

	def __mul__(self, other: "Point"):
		return Point(self.x * other.x, self.y * other.y)

	def __truediv__(self, other: "Point"):
		return Point(self.x / other.x, self.y / other.y)

	@property
	def phi(self):
		return math.atan2(self.y, self.x)

	def distance_to(self, other: "Point"):
		diff = self - other
		return math.hypot(diff.x, diff.y)

	def get_tuple(self):
		return (self.x, self.y)


class Line:
	def __init__(self, p1: Point, p2: Point):
		self.p1 = p1
		self.p2 = p2

		self.a = -(p1 - p2).y
		self.b = (p1 - p2).x
		self.c = -(self.a * p1.x + self.b * p1.y)

	def eval(self, point: Point):
		"""
		Returns positive number if the point is on the one side and negative number if on the other. Otherwise 0
		"""
		return self.a * point.x + self.b * point.y + self.c

	def length(self):
		return self.p1.distance_to(self.p2)

	def contains(self, point: Point) -> bool:
		return (
			math.isclose(point.x * self.a + point.y * self.b + self.c, 0, abs_tol=1e-9)
			and self.p1.distance_to(point) <= self.length()
			and self.p2.distance_to(point) <= self.length()
		)

	def intersection(self, line: "Line") -> Point | None:
		d = self.a * line.b - line.a * self.b

		if d == 0:
			return None

		return Point((self.b * line.c - line.b * self.c) / d, (self.c * line.a - line.c * self.a) / d)


class Rectangle:
	def __init__(self, points: list[Point]):
		if len(points) != 4:
			raise ValueError(f"Four points expected but {len(points)} points were given")
		
		self.points = points
		

class Circle:
	def __init__(self, center: Point, radius: float):
		self.center = center
		self.radius = radius

	def contains(self, point: Point):
		return math.isclose(point.distance_to(self.center), self.radius, abs_tol=1e-9)

	def intersections(self, line: Line) -> list[Point]:
		# Handle degenerate line (point)
		if line.p1.x == line.p2.x and line.p1.y == line.p2.y:
			pt = line.p1
			# Check if the point lies exactly on the circle
			if self.contains(pt):
				return [pt]
			else:
				return []

		# Shift line so circle center is at origin
		a = line.a
		b = line.b
		c = line.c + line.a * self.center.x + line.b * self.center.y

		# Calculate perpendicular distance from center (now at origin) to line
		dist = abs(c) / math.hypot(a, b)

		if dist > self.radius:
			return []

		# Find base point on the line closest to origin
		scale = -c / (a * a + b * b)
		base_x = a * scale
		base_y = b * scale

		if dist == self.radius:
			return [Point(base_x + self.center.x, base_y + self.center.y)]

		# Find offset for the two intersection points
		offset_len = math.sqrt(self.radius**2 - dist**2)
		norm = math.hypot(a, b)
		offset_x = -b * offset_len / norm
		offset_y = a * offset_len / norm

		p1 = Point(base_x + offset_x + self.center.x, base_y + offset_y + self.center.y)
		p2 = Point(base_x - offset_x + self.center.x, base_y - offset_y + self.center.y)

		return [i for i in [p1, p2] if line.contains(i)]


if __name__ == "__main__":
	import pygame
	import sys

	pygame.init()
	screen = pygame.display.set_mode((800, 600))
	pygame.display.set_caption("Geometry Test")
	clock = pygame.time.Clock()

	circle = Circle(Point(400, 300), 150)

	# Interactive line drawing
	lines: list[Line] = []
	drawing = False
	start_pos: tuple[int, int] = (0, 0)

	# Main loop
	running = True
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			elif event.type == pygame.MOUSEBUTTONDOWN:
				start_pos = event.pos
				drawing = True
			elif event.type == pygame.MOUSEBUTTONUP and drawing:
				end_pos = event.pos
				# Create and store the new line
				new_line = Line(Point(start_pos[0], start_pos[1]), Point(end_pos[0], end_pos[1]))
				lines.append(new_line)
				drawing = False

		screen.fill((255, 255, 255))

		# Draw circle
		pygame.draw.circle(screen, "black", circle.center.get_tuple(), circle.radius, width=1)

		# Draw all stored lines and their intersections
		for ln in lines:
			# draw line
			pygame.draw.line(screen, (0, 0, 0), (ln.p1.x, ln.p1.y), (ln.p2.x, ln.p2.y), 2)
			# compute and draw intersections
			inters = circle.intersections(ln)
			for pt in inters:
				pygame.draw.circle(screen, (255, 0, 0), pt.get_tuple(), 5)

		# Preview current drawing line
		if drawing and start_pos:
			curr_pos = pygame.mouse.get_pos()
			pygame.draw.line(screen, (150, 150, 150), start_pos, curr_pos, 1)

		pygame.display.flip()
		clock.tick(60)

	pygame.quit()
	sys.exit()
