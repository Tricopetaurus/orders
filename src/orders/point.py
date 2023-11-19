from __future__ import annotations

import math
from typing import Optional

class Point:
    x: float
    y: float

    def __init__(self, x: float, y: float):
        self.x, self.y = x, y

    def distance(self, p: Point) -> float:
        return math.sqrt((p.x - self.x) ** 2 + (p.y - self.y) ** 2)

    def xy_distance(self, p: Point) -> tuple[float, float]:
        x = p.x - self.x
        y = p.y - self.y
        return (x, y)

    def overshot_by_n(self, dest: Point, next: Point) -> Optional[float]:
        """Assuming 3 pts on a line, calculate how far
        an overshoot (if any) occured by.
        Returns None if no overshot occured
        """
        if self.distance(dest) > self.distance(next):
            return None
        else:
            return dest.distance(next)

    def __str__(self) -> str:
        return f"{self.x:3.03f}, {self.y:3.03f}"

    def __eq__(self, other: Point) -> bool:
        return other.x == self.x and other.y == self.y


