import math
import random

import numpy as np

import stopwatch
from creature import Creature
from selection import is_selected
from visualisation import Visualisation
from world import World


class Simulation:
    def __init__(self, config):
        self.debug = config['application']['debug']
        self.config = config

        if config['simulation']['seed'] > -1:
            random.seed(config['simulation']['seed'])
            np.random.seed(config['simulation']['seed'])

        self.world = World(config)

        self.visualisation = Visualisation(size=config['visualisation']['size'],
                                  framerate=config['visualisation']['framerate'],
                                  interval=config['visualisation']['interval']) \
        if config['visualisation']['on'] else None

        self.creatures = [Creature(config) for _ in range(config['simulation']['n_creatures'])]
        self.born_creatures = []
        self.dead_creatures = []
        self.simulation_step = 0

        self.season_clock = 0


    def left_upper_corner(self):
        print('left_upper_corner')

    def repopulate(self, selection_function):
        survivors = []
        for creature in self.creatures:
            if is_selected(selection_function, creature):
                survivors.append(creature)

        if len(survivors) == 0:
            print("No creatures met the selection criterium, run another epoch with same creatures")
            return

        print(f"{len(survivors) / self.config['simulation']['generation_size'] * 100}% survivors")

        self.creatures = []
        for _ in range(self.config['simulation']['generation_size']):
            survivor = random.choice(survivors)
            self.creatures.append(survivor.reproduce(other=None, same_location=True, share_energy=False))

    def run(self, max_iterations):
        # simulation loop

        # TODO: populate world

        while self.simulation_step < max_iterations:
            self.simulation_step += 1

            # update clock
            t = (self.simulation_step % self.config['simulation']['generation_lifespan']) \
                / self.config['simulation']['generation_lifespan'] * math.pi * 2

            self.season_clock = math.sin(t)


            if self.debug:
                print(f"Simulation step: {self.simulation_step}")


            # force new generation
            if self.config['simulation']['force_new_generation'] \
                    and self.simulation_step % self.config['simulation']['generation_lifespan'] == 0:
                self.repopulate(self.config['simulation']['generation_selection'])

            stopwatch.start("world_update")
            self.world.update()
            stopwatch.stop("world_update")

            stopwatch.start("creatures_update")
            for creature in self.creatures:
                creature.update(self, self.world)
                if creature.state['energy'] < 0:
                    self.dead_creatures.append(creature)
            stopwatch.stop("creatures_update")

            stopwatch.start("creatures_population_changes")
            # add new creatues
            self.creatures += self.born_creatures
            print(f"{len(self.born_creatures)} born")
            self.born_creatures = []

            # remove old creatures
            for creature in self.dead_creatures:
                self.creatures.remove(creature)
            self.dead_creatures = []

            # cleanup if there are more creatures than allowed
            if len(self.creatures) > self.config['simulation']['max_creatures']:
                self.creatures = self.creatures[0:self.config['simulation']['max_creatures']]

            # prevent extinction
            while len(self.creatures) < self.config['simulation']['min_creatures']:
                self.creatures.append(Creature(self.config))
            stopwatch.stop("creatures_population_changes")

            stopwatch.start("visualisation")
            # show
            if self.visualisation is not None:
                self.visualisation.update(self.world, self.creatures)

            print(f"{len(self.creatures)} creatures")
            stopwatch.stop("visualisation")

    def add_creature(self, creature):
        self.born_creatures.append(creature)

    def move(self, position):
        x = max(0, min(position[0], self.config['world_parameters']['size'] - 1))
        y = max(0, min(position[1], self.config['world_parameters']['size'] - 1))
        return (x, y)
