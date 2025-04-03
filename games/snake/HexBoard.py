import pygame

from .HexCell import HexCell


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

    def draw(self, surface: pygame.Surface, cell_numbers: bool = False) -> None:
        """
        Draws all hex cells onto the given pygame surface.
        """
        if cell_numbers:
            font = pygame.font.SysFont(None, 24)

        for cell in self.cells:
            center = cell.axial_to_pixel(self.cell_size, self.offset)
            points = cell.get_polygon_points(center, self.cell_size)
            pygame.draw.polygon(surface, (200, 200, 200), points, 2)

            if cell_numbers:
                text = font.render(f"{cell.q},{cell.r}", True, (255, 255, 255))
                text_rect = text.get_rect(center=center)
                surface.blit(text, text_rect)
