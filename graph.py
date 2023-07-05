import matplotlib.pyplot as plt
import matplotlib

# needed to escape sciview in pycharm
# tkinter backend is not compatible with pygame
# https://matplotlib.org/stable/users/explain/backends.html
matplotlib.use('macosx')
import numpy as np


class Graph:
    def __init__(self):
        # enable interactive mode
        # https://www.geeksforgeeks.org/how-to-update-a-plot-on-same-figure-during-the-loop/
        plt.ion()

        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)
        self.t = []
        self.n = []

        self.rabbits, = self.ax.plot(self.t, self.n)

        plt.xlabel("timesteps")
        plt.ylabel("number of rabbits")
        plt.title("rabbit simulation")

    def update(self, word, creatures, simulation):
        self.t.append(simulation.simulation_step)
        self.n.append(len(simulation.creatures))

        self.rabbits.set_xdata(self.t)
        self.rabbits.set_ydata(self.n)

        plt.xlim([0, simulation.simulation_step])
        plt.ylim([0, max(self.n)])
        self.fig.canvas.draw()

        # to flush the GUI events
        self.fig.canvas.flush_events()

        pass





