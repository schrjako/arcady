import pygame


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
