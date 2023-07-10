import random

import numpy as np

from world import World


def heartbeat(simulation, world, creature):
    return [0] if simulation.simulation_step % creature.state['properties']['heartbeat'] > 0 else [1]

def look_for_grass(simulation, world, creature):
    information = world.give_information_about_location(creature.state['position'][0, 0], creature.state['position'][1, 0])

    # filter grass only (for now)
    information = np.equal(information, world.GRASS).astype(int)

    return information

def look_for_rabbit(simulation, world, creature):
    information = world.give_information_about_location(creature.state['position'][0, 0], creature.state['position'][1, 0])

    # filter grass only (for now)
    information = np.equal(information, world.RABBIT).astype(int)

    return information

def has_no_neighbours(simulation, world, creature):
    information = world.give_information_about_animals(creature.state['position'][0, 0], creature.state['position'][1, 0])

    # remove self from information
    information[4] = 0
    # filter grass only (for now)
    neighbours = np.sum(information)

    has_no_neighbours = np.equal(neighbours, 0).astype(int)

    return has_no_neighbours

def is_not_standing_on_grass(simulation, world, creature):
    information = world.give_information_about_location(creature.state['position'][0, 0], creature.state['position'][1, 0])
    return [1] if information != World.GRASS else [0]

def energy_level(simulation, world, creature):
    return creature.state['energy']

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
