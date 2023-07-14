import matplotlib.pyplot as plt
import matplotlib

# needed to escape sciview in pycharm
# tkinter backend is not compatible with pygame
# https://matplotlib.org/stable/users/explain/backends.html
matplotlib.use('macosx')
import numpy as np


class Graph:
    def __init__(self, species):
        # enable interactive mode
        # https://www.geeksforgeeks.org/how-to-update-a-plot-on-same-figure-during-the-loop/
        plt.ion()

        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)
        self.t = []

        self.n = {}
        self.plots = {}

        self.species_names = []
        for s in species:
            self.species_names.append(s[0])

        for species in self.species_names:
            self.n[species] = []
            self.plots[species], = self.ax.plot(self.t, self.n[species], label = species)

        plt.legend()
        plt.xlabel("timesteps")
        plt.ylabel("number of creatures")
        plt.title("world simulation")

    def update(self, word, creatures, simulation):
        self.t.append(simulation.simulation_step)

        ylim = 0
        for species in self.species_names:
            print(species)
            self.n[species].append(simulation.count[species])
            self.plots[species].set_xdata(self.t)
            self.plots[species].set_ydata(self.n[species])
            ylim = max(ylim, max(self.n[species]))

        plt.xlim([0, simulation.simulation_step])
        plt.ylim([0, ylim])
        self.fig.canvas.draw()

        # to flush the GUI events
        self.fig.canvas.flush_events()

        pass





