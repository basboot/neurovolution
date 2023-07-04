import random

import numpy as np

from world import World


def heartbeat(simulation, world, creature):
    return [0] if simulation.simulation_step % creature.state['properties']['heartbeat'] > 0 else [1]

def look(simulation, world, creature):
    information = world.give_information_about_location(int(creature.state['position'][0]),
                                                        int(creature.state['position'][1]))

    # filter grass only (for now)
    information = np.equal(information, world.GRASS).astype(int)

    return information

def is_not_standing_on_grass(simulation, world, creature):
    information = world.give_information_about_location(int(creature.state['position'][0]),
                                                        int(creature.state['position'][1]))
    return [1] if information != World.GRASS else [0]

def energy_level(simulation, world, creature):
    return creature.state['energy']

def find_middle(simulation, world, creature):
    x_middle = creature.config['world_parameters']['size'] / 2
    y_middle = creature.config['world_parameters']['size'] / 2
    x = creature.state['position'][0]
    y = creature.state['position'][1]

    return [int(x < x_middle), int(x > x_middle), int(y < y_middle), int(y > y_middle)]

def four_random_values(simulation, world, creature):
    return np.random.uniform(-1, 1, (4, 1))

def random_0_or_1(simulation, world, creature):
    return [1] if random.random() < 0.5 else [0]

def always_on(simulation, world, creature):
    return [1]

def internal_clock(simulation, world, creature):
    return simulation.season_clock

def get_position(simulation, world, creature):
    # return  normalized position
    return creature.state['position'] / creature.config['world_parameters']['size']


def use_sensor(name, n_values, active, simulation, world, creature):
    if active:
        return globals()[name](simulation, world, creature)
    else:
        return [0] * n_values
