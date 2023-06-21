import numpy as np

from world import World


def heartbeat(simulation, world, creature):
    return [0] if simulation.simulation_step % creature.state['properties']['heartbeat'] > 0 else [1]

def is_standing_on_grass(simulation, world, creature):
    information = world.give_information_about_location(int(creature.state['position'][0]),
                                                        int(creature.state['position'][1]))
    return [1] if information == World.GRASS else [0]

def find_middle(simulation, world, creature):
    x_middle = creature.config['world_parameters']['size'] / 2
    y_middle = creature.config['world_parameters']['size'] / 2
    x = creature.state['position'][0]
    y = creature.state['position'][1]

    return [int(x < x_middle), int(x > x_middle), int(y < y_middle), int(y > y_middle)]

def four_random_values(simulation, world, creature):
    return [np.random.random() * 1.0 for _ in range(4)]


def use_sensor(name, n_values, active, simulation, world, creature):
    if active:
        return globals()[name](simulation, world, creature)
    else:
        return [0] * n_values
