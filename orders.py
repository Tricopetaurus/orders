from __future__ import annotations

import csv
import math
from typing import Optional

import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from matplotlib.animation import FuncAnimation

# Self-animate if False
USE_SLIDER = False

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


class Courier:
    _loc: Point
    _step_size: float
    _waypoints: list[tuple[Point, Optional[float]]]
    _clock_time: float 
    _speed : float

    def __init__(self, p: Point, leave_at_t: Optional[float] = None, step_size: float = 1.0, speed: float = 1.0):
        self._clock_time = 0
        self._loc = p
        self._waypoints = list()
        self._step_size = step_size
        self._speed = speed
        self.add_waypoint(p, leave_at_t)

    @property
    def loc(self) -> Point:
        return self._loc

    def add_waypoint(self, p: Point, leave_at_t: Optional[float] = None):
        self._waypoints.append((p, leave_at_t))

    def add_many_waypoints(self, list_of_p: list[tuple[Point, float]]):
        self._waypoints.extend(list_of_p)

    def distance_to_complete(self) -> float:
        total_distance = 0.0
        a = [self.loc, *self._waypoints]
        b = a[1:]
        for _a, _b in zip(a, b):
            total_distance += _a.distance(_b)
        return total_distance

    def steps_to_complete(self) -> int:
        return math.ceil(self.distance_to_complete() / self._step_size)

    def next_point(self) -> Optional[Point]:
        if len(self._waypoints):
            return self._waypoints[0][0]
        print("No more points!")
        return None

    def next_leave_t(self) -> Optional[float]:
        if len(self._waypoints):
            return self._waypoints[0][1]
        print("No more points!")
        return None

    # Advance point 1 more towards next waypoint
    def advance(self):
        self._clock_time += self._step_size
        next = self.next_point()
        next_leave_t = self.next_leave_t()
        # wait right here until it's time to leave 
        if next_leave_t and self._clock_time < next_leave_t:
            return
        if not next:
            return
        x, y = self._loc.xy_distance(next)
        angle_to_target = math.atan2(y, x)
        next_x = self._loc.x + self._step_size * self._speed * math.cos(angle_to_target)
        next_y = self._loc.y + self._step_size * self._speed * math.sin(angle_to_target)
        next_point = Point(next_x, next_y)
        overshoot = self.loc.overshot_by_n(next, next_point)
        if overshoot:
            print(f"overshot by {overshoot:.2f}")
            self._loc = next
            self._waypoints = self._waypoints[1:]
            # TODO: Apply remainder towards NEXT
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
        return f"x: {self.loc.x:3.02f} y: {self.loc.y:3.02f}"

def load_csv(path: str) -> list[dict]:
    with open(path) as f:
        dict_reader = csv.DictReader(f)
        return [row for row in dict_reader]


def float_or_none(s: str) -> Optional[float]:
    try:
        return float(s)
    except ValueError:
        return None

def plot_matplotlib(clist: list[dict]):
    couriers = {}

    for row in clist:
        c_name = row['courier']
        if c_name not in couriers:
            couriers[c_name] = []
        try:
            couriers[c_name].append((float(row['x']), float(row['y']), float_or_none(row['time'])))
        except ValueError:
            pass

    COURIER_SPEED = 320     # Meters per Minute
    STEP_SIZE = .25

    # Grab the first point from each of our dictionary entries
    # To use as the courier's origin point / constructor
    all_couriers = []
    colors = ["green"]

    fig, ax = plt.subplots()

    ax.axis([0, 15000, 0, 12000])
    ax.set_aspect(1)  # x y
    plt.grid(True)

    for key in couriers:
        color_marker = 0
        try:
            x, y = couriers[key][0][0], couriers[key][0][1]
            time = couriers[key][0][2]
        except:
            continue
        new_courier = Courier(Point(x, y), time, step_size=STEP_SIZE, speed=COURIER_SPEED)
        for x, y, t in couriers[key][1:]:
            new_courier.add_waypoint(Point(x, y), t)
            ax.plot(x, y, c=colors[color_marker], marker="x")
            color_marker = min(color_marker + 1, len(colors) - 1)
        all_couriers.append(new_courier)

    all_courier_pts = [c.get_all_points() for c in all_couriers]
    MAX_T = len(max(all_courier_pts, key=lambda pts: len(pts)))

    # Make room at the bottom for sliders
    fig.subplots_adjust(bottom=0.3)
    courier_dots = []
    for c in all_courier_pts:
        (dot,) = ax.plot(
            c[0].x, c[0].y, c="red", marker="o", ms=10
        )  # plot the red point
        courier_dots.append(dot)

    def update_plot(t: int):
        for idx, dot in enumerate(courier_dots):
            _t = int(min(t, len(all_courier_pts[idx]) - 1))
            new_x = all_courier_pts[idx][_t].x
            new_y = all_courier_pts[idx][_t].y
            dot.set_xdata([new_x])
            dot.set_ydata([new_y])

    def update_t(t):
        update_plot(t)
        fig.canvas.draw_idle()

    if USE_SLIDER:
        # Create slider and create Axes for the sliders
        axcolor = "#909090"
        sax_y = plt.axes([0.25, 0.15, 0.65, 0.03], facecolor=axcolor)
        st = Slider(sax_y, "Time", valmin=0, valmax=MAX_T)

        # Tell sliders which function to call when changed
        st.on_changed(update_t)
        plt.show()
    else:
        t = FuncAnimation(fig=fig, func=update_plot, frames=list(range(MAX_T)), interval=1, repeat_delay=1000)
        plt.show()


if __name__ == "__main__":
    couriers = load_csv('./orders.csv')
    plot_matplotlib(couriers)
