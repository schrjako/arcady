import pygame

import math


def draw_cube(
	surface: pygame.Surface,
	colors: (
		tuple[pygame.Color, pygame.Color, pygame.Color]
		| tuple[tuple[int, int, int], tuple[int, int, int], tuple[int, int, int]]
	),
	points: list[tuple[float, float]],
	center: tuple[float, float],
):
	# Colors: right, left, top
	pygame.draw.polygon(surface, colors[0], points[:3] + [center])
	pygame.draw.polygon(surface, colors[1], points[2:5] + [center])
	pygame.draw.polygon(surface, colors[2], points[4:6] + [points[0], center])


def draw_reg_polygon(
	surface: pygame.Surface,
	color: pygame.Color | tuple[int, int, int],
	number_of_edges: int,
	center: tuple[float, float],
	radius: float,
	rotation: int = 180,
):
	points = []

	for i in range(number_of_edges):
		angle = math.radians(i * 360 / number_of_edges + rotation)
		points.append(
			[
				round(center[0] + math.sin(angle) * radius),
				round(center[1] + math.cos(angle) * radius),
			]
		)

	pygame.draw.polygon(surface, color, points)
