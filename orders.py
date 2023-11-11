from __future__ import annotations
import math
from typing import Optional

class Point:
    x: float
    y: float

    def __init__(self, x: float, y: float):
        self.x, self.y = x, y

    def distance(self, p: Point) -> float:
        return math.sqrt(
            (p.x - self.x)**2 + (p.y - self.y)**2
        )

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
        return f'{self.x:3.03f}, {self.y:3.03f}'

    def __eq__(self, other: Point) -> bool:
        return other.x == self.x and other.y == self.y


class Courier:
    _loc: Point
    _step_size: float
    _waypoints: list[Point]

    def __init__(self, p: Point, step_size: float = 1.0):
        self._loc = p
        self._waypoints = list()
        self._step_size = step_size

    @property
    def loc(self) -> Point:
        return self._loc
    
    def add_waypoint(self, p: Point):
        self._waypoints.append(p)

    def distance_to_complete(self) -> float:
        total_distance = 0.0
        a = [self.loc, *self._waypoints]
        b = a[1:]
        for _a,_b in zip(a, b):
            total_distance += _a.distance(_b)
        return total_distance

    def steps_to_complete(self) -> int:
        return math.ceil(self.distance_to_complete() / self._step_size)

    def next_point(self) -> Optional[Point]:
        if len(self._waypoints):
            return self._waypoints[0]
        print('No more points!')
        return None

    # Advance point 1 more towards next waypoint
    def advance(self):
        next = self.next_point()
        if not next:
            return
        x, y = self._loc.xy_distance(next)
        angle_to_target = math.atan2(y, x)
        next_x = self._loc.x + self._step_size * math.cos(angle_to_target)
        next_y = self._loc.y + self._step_size * math.sin(angle_to_target)
        next_point = Point(next_x, next_y)
        overshoot = self.loc.overshot_by_n(next, next_point)
        if overshoot:
            print(f"overshot by {overshoot:.2f}")
            self._loc = next
            self._waypoints = self._waypoints[1:]
            # TODO: Apply remainder towards NEXT NEXT
            # Need to set step size to remainder, pop 
        else:
            self._loc = next_point

    # Calls advance until empty
    def get_all_points(self):
        points = []
        while len(self._waypoints):
            points.append(self.loc)
            self.advance()
        points.append(self.loc)
        return points


    def __str__(self):
        return f'x: {self.loc.x:3.02f} y: {self.loc.y:3.02f}'






def main():
    origin = Point(0,0)
    p1 = Point(3,4)
    p2 = Point(2,6)
    c1 = Courier(origin, .6)
    c1.add_waypoint(p1)
    c1.add_waypoint(p2)
    p3 = Point(9, 2)
    p4 = Point(1, 1)
    c2 = Courier(origin, .6)
    c2.add_waypoint(p3)
    c2.add_waypoint(p4)
    # steps = c.steps_to_complete()
    all_c1 = c1.get_all_points()
    all_c2 = c2.get_all_points()
    for c1, c2 in zip(all_c1, all_c2):
        print(f'{"*" if c1==p1 or c1==p2 else " "}c1: {c1}  {"*" if c2==p3 or c2==p4 else " "}c2: {c2}')

    for c2 in all_c2[len(all_c1):]:
        print(f'{" "*19}{"*" if c2==p3 or c2==p4 else " "}c2: {c2}')

if __name__ == '__main__':
    main()

