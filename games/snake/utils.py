import pygame

import math


def draw_cube(
	surface: pygame.Surface,
	points: list[tuple[float, float]],
	center: tuple[float, float],
	colors: (
		tuple[pygame.Color, pygame.Color, pygame.Color]
		| tuple[tuple[int, int, int], tuple[int, int, int], tuple[int, int, int]]
	),
):
	# Colors: right, left, top
	pygame.draw.polygon(surface, colors[0], points[:3] + [center])
	pygame.draw.polygon(surface, colors[1], points[2:5] + [center])
	pygame.draw.polygon(surface, colors[2], points[4:6] + [points[0], center])


def draw_triangle(
	surface: pygame.Surface,
	center: tuple[float, float],
	radius: float,
	color: pygame.Color | tuple[int, int, int],
):
	points = [
		[
			center[0] + math.sin(math.radians(i)) * radius,
			center[1] + math.cos(math.radians(i)) * radius,
		]
		for i in range(180, 540, 120)
	]
	pygame.draw.polygon(surface, color, points)
