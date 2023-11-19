from __future__ import annotations

import csv
from typing import Optional

import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from matplotlib.animation import FuncAnimation

from .courier import Courier, WayPoint

# Self-animate if False
USE_SLIDER = False

COURIER_SPEED = 320  # Meters per Minute
STEP_SIZE = 0.25


def load_csv(path: str) -> list[Courier]:
    clist = []
    with open(path) as f:
        dict_reader = csv.DictReader(f)
        clist.extend([row for row in dict_reader if len(row.keys())])

    couriers = {}
    for row in clist:
        c_name = row["courier"]
        if c_name not in couriers:
            couriers[c_name] = []
        try:
            couriers[c_name].append(
                (float(row["x"]), float(row["y"]), float_or_none(row["time"]), row["where to"])
            )
        except ValueError:
            pass

    all_couriers = []
    for key in couriers:
        try:
            x, y = couriers[key][0][0], couriers[key][0][1]
            time = couriers[key][0][2]
            name = couriers[key][0][3]
        except IndexError:
            continue
        new_courier = Courier(
            WayPoint(x, y, time, name), step_size=STEP_SIZE, speed=COURIER_SPEED
        )
        for args in couriers[key][1:]:
            new_courier.add_waypoint(WayPoint(*args))
        all_couriers.append(new_courier)

    return all_couriers


def float_or_none(s: str) -> Optional[float]:
    try:
        return float(s)
    except ValueError:
        return None


def plot_matplotlib(couriers: list[Courier]):
    # Grab the first point from each of our dictionary entries
    # To use as the courier's origin point / constructor
    colors = ["green", "deepskyblue", "lightcoral", "gold", "orangered", "violet", "hotpink", "sandybrown", "purple", "darkblue"]
    color_marker = 0

    fig, ax = plt.subplots()

    ax.axis([0, 15000, 0, 12000])
    ax.set_aspect(1)  # x y
    plt.grid(True)

    courier_dots = []
    for c in couriers:
        color = colors[color_marker]
        (dot,) = ax.plot(
            c.loc.x, c.loc.y, c=color, marker="o", ms=10
        )  # plot the red point
        courier_dots.append(dot)
        for wp in c.waypoints[1:]:
            marker = '$?$'
            if wp.name:
                marker = "*" if wp.name.startswith('r') else "."
                color = "red" if wp.name.startswith('r') else colors[color_marker]
            ax.plot(wp.x, wp.y, c=color, marker=marker)
        color_marker = (color_marker + 1) % len(colors)

    all_courier_pts = [c.get_all_points() for c in couriers]
    MAX_T = len(max(all_courier_pts, key=lambda pts: len(pts)))

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
        # Make room at the bottom for sliders
        fig.subplots_adjust(bottom=0.3)
        # Create slider and create Axes for the sliders
        axcolor = "#909090"
        sax_y = plt.axes([0.25, 0.15, 0.65, 0.03], facecolor=axcolor)
        st = Slider(sax_y, "Time", valmin=0, valmax=MAX_T)

        # Tell sliders which function to call when changed
        st.on_changed(update_t)
        plt.show()
    else:
        t = FuncAnimation(
            fig=fig,
            func=update_plot,
            frames=list(range(MAX_T)),
            interval=1,
            repeat_delay=1000,
        )
        plt.show()


def main(orders_path: str):
    couriers = load_csv(orders_path)
    plot_matplotlib(couriers)
