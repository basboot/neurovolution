import math
import random

import numpy as np
import pygame

import stopwatch
from creature import Creature
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

        self.creatures = [Creature(config, self.world, config['creatures']['species'][0]) for _ in range(config['simulation']['n_creatures'])]
        self.born_creatures = []
        self.dead_creatures = []
        self.simulation_step = 0

        self.season_clock = 0
        self.generation = 0


    def left_upper_corner(self):
        print('left_upper_corner')

    def run(self, max_iterations):
        # simulation loop

        # TODO: populate world

        while self.simulation_step < max_iterations:
            self.simulation_step += 1

            # update clock
            t = (self.simulation_step % self.config['simulation']['season_iterations']) \
                / self.config['simulation']['season_iterations'] * math.pi * 2

            self.season_clock = math.sin(t)


            if self.debug:
                print(f"Simulation step: {self.simulation_step}")

            stopwatch.start("world_update")
            self.world.update()
            stopwatch.stop("world_update")

            stopwatch.start("creatures_update")
            for creature in self.creatures:
                creature.update(self, self.world)
                # creatures die when they have no energy
                if creature.state['energy'] < 0:
                    self.dead_creatures.append(creature)
                # creatures die when they are too old
                if creature.state['age'] > creature.config['creature'][creature.species]['max_age']:
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
                self.creatures.append(Creature(self.config, self.world, self.config['creatures']['species'][0]))
            stopwatch.stop("creatures_population_changes")

            stopwatch.start("visualisation")
            # show
            if self.visualisation is not None:
                self.visualisation.update(self.world, self.creatures, self)

            print(f"{len(self.creatures)} creatures")
            stopwatch.stop("visualisation")

    def add_creature(self, creature):
        self.born_creatures.append(creature)

    def move(self, position):
        return np.clip(position, 0, self.config['world_parameters']['size'] - 1)

    def draw_simulation(self, screen):
        font = pygame.font.SysFont('arial', int(self.config['visualisation']['size'][0] * 0.0625))
        text_surface = font.render(f"t = {self.simulation_step}", False, (0, 0, 0))
        screen.blit(text_surface, (10, 10))
