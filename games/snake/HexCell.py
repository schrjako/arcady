import math


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
