import math
import random

import numpy as np
import pygame

import stopwatch
from creature import Creature
from graph import Graph
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

        self.visualisation = Visualisation(config['visualisation']['scaling'], size=(config['world_parameters']['size'], config['world_parameters']['size']),
                                  framerate=config['visualisation']['framerate'],
                                  interval=config['visualisation']['interval'],
                                           visualise_eating=config['visualisation']['visualise_eating']) \
        if config['visualisation']['on'] else None

        self.graph = Graph() \
            if config['graph']['on'] else None

        self.creatures = []

        for species in config['creatures']['species']:
            for _ in range(config['creature'][species[0]]['n_creatures']):
                self.creatures.append(Creature(config, self.world, species))

        self.born_creatures = []
        self.dead_creatures = set() # use set to prevent double removals
        self.simulation_step = 0

        self.season_clock = 0
        self.generation = 0

        self.count = {
            "rabbit": 0,
            "wolve": 0
        }

        self.killed = []


    def left_upper_corner(self):
        print('left_upper_corner')

    def run(self, max_iterations):
        # simulation loop

        # TODO: populate world

        while self.simulation_step < max_iterations:
            self.count = {
                "rabbit": 0,
                "wolve": 0
            }
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
                self.count[creature.species] += 1
                creature.update(self, self.world)

            # add new creatues
            self.creatures += self.born_creatures
            print(f"{len(self.born_creatures)} born")
            self.born_creatures = []

            # find dead creatures after all updates
            for creature in self.creatures:
                # creatures die when they have no energy
                if creature.state['energy'] < 0:
                    self.dead_creatures.add(creature)
                # creatures die when they are too old
                if creature.state['age'] > creature.config['creature'][creature.species]['max_age']:
                    self.dead_creatures.add(creature)

            stopwatch.stop("creatures_update")

            stopwatch.start("creatures_population_changes")
            # prevent extinction
            while len(self.creatures) < self.config['simulation']['min_creatures']:
                # select random species
                species = self.config['creatures']['species']
                selected_species =  random.choice(species)
                self.creatures.append(Creature(self.config, self.world, selected_species))
                self.count[selected_species[0]] += 1
            stopwatch.stop("creatures_population_changes")

            stopwatch.start("visualisation")
            # show
            if self.visualisation is not None:
                self.visualisation.update(self.world, self.creatures, self)
            if self.graph is not None:
                self.graph.update(self.world, self.creatures, self)

            print(f"{len(self.creatures)} creatures")
            stopwatch.stop("visualisation")

            # remove old creatures
            for creature in self.dead_creatures:
                self.count[creature.species] -= 1
                # cleanup world grid
                self.world.remove_animal(creature.state['position'])
                # cleanup creature
                self.creatures.remove(creature)
            self.dead_creatures = set()
            self.killed = []

    def add_creature(self, creature):
        self.born_creatures.append(creature)

    def move(self, position):
        return np.clip(position, 0, self.config['world_parameters']['size'] - 1)

    def draw_simulation(self, screen, killed=False):
        if self.config['visualisation']['scaling'] < 5:
            font = pygame.font.SysFont('arial', int(self.config['world_parameters']['size'] * 0.0625))
            text_surface = font.render(f"t = {self.simulation_step}, r = {self.count['rabbit']}, w = {self.count['wolve']}", False, (0, 0, 0))
            screen.blit(text_surface, (10, 10))

        if killed:
            for killed_creature in self.killed:
                pass
                screen.set_at((killed_creature[0, 0], killed_creature[1, 0]), (0, 0, 0))
