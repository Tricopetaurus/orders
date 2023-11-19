import math
from copy import deepcopy
from typing import Optional

from .point import Point


class WayPoint(Point):
    time: Optional[float]
    name: Optional[str]

    def __init__(
        self,
        x: float,
        y: float,
        time: Optional[float] = None,
        name: Optional[str] = None,
    ):
        super().__init__(x, y)
        self.time = time
        self.name = name


class Courier:
    _loc: Point
    _step_size: float
    _waypoints: list[WayPoint]
    _clock_time: float
    _speed: float
    _name: str

    def __init__(
        self,
        wp: WayPoint,
        step_size: float = 1.0,
        speed: float = 1.0,
        name: str = 'c?'
    ):
        self._clock_time = 0
        self._loc = wp
        self._waypoints = list()
        self._step_size = step_size
        self._speed = speed
        self.name = name
        self.add_waypoint(wp)

    @property
    def loc(self) -> Point:
        return self._loc

    @property
    def waypoints(self) -> list[WayPoint]:
        return deepcopy(self._waypoints)

    def add_waypoint(self, wp: WayPoint):
        self._waypoints.append(wp)

    def add_many_waypoints(self, list_of_wp: list[WayPoint]):
        self._waypoints.extend(list_of_wp)

    def distance_to_complete(self) -> float:
        total_distance = 0.0
        a = [self.loc, *self._waypoints]
        b = a[1:]
        for _a, _b in zip(a, b):
            total_distance += _a.distance(_b)
        return total_distance

    def steps_to_complete(self) -> int:
        return math.ceil(self.distance_to_complete() / self._step_size)

    def next_point(self) -> Optional[WayPoint]:
        if len(self._waypoints):
            return self._waypoints[0]
        return None

    def step_to(self, next: Point, step: Optional[float] = None) -> Optional[float]:
        step = self._step_size * self._speed if step is None else step
        angle_to_target = self._loc.angle_to(next)
        next_x = self._loc.x + step * math.cos(angle_to_target)
        next_y = self._loc.y + step * math.sin(angle_to_target)
        next_point = Point(next_x, next_y)
        overshoot = self.loc.overshot_by_n(next, next_point)
        if overshoot:
            self._loc = next
        else:
            self._loc = next_point
        return overshoot

    # Advance point 1 more towards next waypoint
    def advance(self):
        self._clock_time += self._step_size
        next = self.next_point()

        # Condition: Done
        if not next:
            return

        # Condition: Currently at destination
        if self._loc == next:

            # ... done waiting
            if (next.time is not None 
                    and self._clock_time >= next.time):
                self._waypoints = self._waypoints[1:]
                next = self.next_point()

            # ... we don't have a timer
            elif next.time is None:
                self._waypoints = self._waypoints[1:]
                next = self.next_point()

            # We do have a timer and we're not done waiting
            else:
                return

        # Condition: Done
        if not next:
            return

        # Warning condition: We're late!
        if (next.time is not None
                and self._clock_time >= next.time):
            print(f"Running late for {next.name}")

        self.step_to(next)

    # Calls advance until empty
    def get_all_points(self):
        points = []
        while len(self._waypoints):
            points.append(self.loc)
            self.advance()
        points.append(self.loc)
        return points

    def __str__(self):
        return f"x: {self.loc.x:3.02f} y: {self.loc.y:3.02f}"
