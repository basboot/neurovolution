import math
import random

import numpy as np
import pygame

import stopwatch
from creature import Creature
from selection import is_selected, get_selection_weight
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
        self.generation = 0


    def left_upper_corner(self):
        print('left_upper_corner')

    def repopulate(self, selection_function):
        self.generation += 1
        print(f"START GENERATION {self.generation}")
        if not self.config['simulation']['weighted_selection']:
            self.repopulate_no_weights(selection_function)

        else:
            weights = []
            for creature in self.creatures:
                weights.append(get_selection_weight(selection_function, creature))

            survivors = self.creatures


            self.creatures = []
            while len(self.creatures) < self.config['simulation']['generation_size']:
                # use k = 1, so it is easier to mix strategies
                survivor = random.choices(survivors, weights=weights, k=1)[0]

                if survivor.state['properties']['ploidy'] == 1:
                    self.creatures.append(survivor.reproduce(other=None, same_location=True, share_energy=False))
                else:
                    if survivor.state['properties']['ploidy'] == 2:
                        # this must be optimized
                        # find mate
                        mate = None
                        while mate is None or mate.state['properties']['ploidy'] != 2:
                            mate = random.choices(survivors, weights=weights, k=1)[0]
                            self.creatures.append(survivor.reproduce(other=mate.state['dna'], same_location=True, share_energy=False))


    def repopulate_no_weights(self, selection_function):
        survivors = []
        for creature in self.creatures:
            if is_selected(selection_function, creature):
                survivors.append(creature)

        print(f"{len(survivors) / self.config['simulation']['generation_size'] * 100}% survivors")
        self.creatures = []

        if len(survivors) == 0:
            print("No creatures met the selection criterium, restart sim")
            self.creatures = []
            for _ in range(self.config['simulation']['generation_size']):
                self.creatures.append(Creature(self.config))
        else:
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
                self.visualisation.update(self.world, self.creatures, self)

            print(f"{len(self.creatures)} creatures")
            stopwatch.stop("visualisation")

    def add_creature(self, creature):
        self.born_creatures.append(creature)

    def move(self, position):
        return np.clip(position, 0, self.config['world_parameters']['size'] - 1)

    def draw_simulation(self, screen):
        if self.config['simulation']['force_new_generation']:
            font = pygame.font.SysFont('arial', 32)
            text_surface = font.render(f"generation {self.generation}", False, (0, 0, 0))
            screen.blit(text_surface, (10, 10))
