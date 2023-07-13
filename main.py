from sys import exit
from functions import *
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from datetime import date, datetime, timedelta
import numpy as np


class CosmicObject: # define individual planets
    def __init__(self, name, rad, color, r, v):
        self.name = name
        self.r = np.array(r, dtype=float)  # radius vectors
        self.v = np.array(v, dtype=float)  # speed vectors
        self.xs = []  # x positions
        self.ys = []  # y positions
        # animation properties
        self.plot = ax.scatter(r[0], r[1], color=color, s=rad ** 2, edgecolors=None, zorder=10)
        (self.line,) = ax.plot([], [], color=color, linewidth=1.4)


class SolarSystem:
    def __init__(self):
        self.planets = []
        self.time = None
        # property
        self.timestamp = ax.text(0.3, 0.94, "Data: ", color="w", transform=ax.transAxes, fontsize="x-large")

    def add_planet(self, planet):
        # adding planet
        self.planets.append(planet)

    def evolve(self):
        # calculating trajectory points
        dt = 1
        self.time += timedelta(dt)
        plots = []
        lines = []
        for i, planet in enumerate(self.planets):
            # calculate radius vectors
            planet.r += planet.v * dt
            # calculating acceleration in AU
            acc = -2.959e-4 * planet.r / np.sum(planet.r ** 2) ** (3 / 2)
            # calculating seed vectors
            planet.v += acc * dt
            # adding x, y and graph shift
            planet.xs.append(planet.r[0])
            planet.ys.append(planet.r[1])
            # adding next animation element
            planet.plot.set_offsets(planet.r[:2])
            plots.append(planet.plot)
            planet.line.set_xdata(planet.xs)
            planet.line.set_ydata(planet.ys)
            # adding next line piece
            lines.append(planet.line)
            # Safety stop to prevent memory overflow
            if len(planet.xs) > 10000:
                raise SystemExit("To prevent ram overflow")

            # we set the date text to the next day
            self.timestamp.set_text(f"Data: {self.time.isoformat()}")
            # return necessary values for animation
            return plots + lines + [self.timestamp]


load_module_ok = True

try:
    import numpy as np
    ok_module_info("numpy")
except:
    error_module_info("numpy")
    load_module_ok = False

try:
    import matplotlib
    ok_module_info("matplotlib")
except:
    error_module_info("matplotlib")
    load_module_ok = False

try:
    from astropy.time import Time
    ok_module_info("astropy")
except:
    error_module_info("astropy")
    load_module_ok = False

try:
    from astroquery.jplhorizons import Horizons
    ok_module_info("astroquery")
except:
    error_module_info("astroquery")
    load_module_ok = False

if not load_module_ok:
    print("Unfortunately something went wrong.")
    print("Closing program.")
    exit(0)

print("Everything is ready.")

nasaids = [1, 2, 3, 4]  # id numbers in NASA database
names = ["Mercury", "Venus", "Earth", "Mars"]
colors = ["gray", "orange", "green", "chocolate"]
sizes = [0.38, 0.95, 1.0, 0.53]
texty = [0.47, 0.73, 1, 1.5]
planet_datas = get_horizon_data(nasaids, names, colors, sizes)

# window application
plt.style.use("dark_background")
fig = plt.figure(
    planet_datas["info"], figsize=[8, 8]
)
ax = plt.axes([0.0, 0.0, 1.0, 1.0], xlim=(-1.8, 1.8), ylim=(-1.8, 1.8))

# creating solar system
CosmicObject("Sun", 28, "yellow", [0, 0, 0], [0, 0, 0])
solar_system = SolarSystem()
solar_system.time = datetime.strptime(planet_datas["date"], "%Y-%m-%d").date()

# generating animation data
for nasaid in nasaids:
    planet = planet_datas[nasaid]

    # adding planet to solar system
    solar_system.add_planet(
        CosmicObject(
            planet["name"],
            planet["size"],
            planet["color"],
            planet["r"],
            planet["v"],
        )
    )

    # adding planet name to animation window
    ax.text(
        0,
        -(texty[nasaid - 1] + 0.1),
        planet["name"],
        color=planet["color"],
        zorder=1000,
        ha="center",
        fontsize="large",
    )


def animate(i):
    return solar_system.evolve()


solar_animation = animation.FuncAnimation(
    fig,
    animate,
    repeat=False,
    frames=365,
    blit=True,
    interval=10,
)

plt.show()


