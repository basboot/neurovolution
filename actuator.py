import random

import numpy as np

from world import World


def move(simulation, world, creature, signals):
    # world does not allow floats
    signals = np.round(signals)
    # combine signals to get desired delta / new position
    desired_move = np.array([signals[0] - signals[1], signals[2] - signals[3]], dtype='int64')
    desired_position = creature.state['position'] + desired_move

    # make sure position in still inside simulation
    desired_position = simulation.move(desired_position)

    # check if world allows move
    if world.move_animal(creature.state['position'], desired_position, animal=creature):
        creature.state['position'] = desired_position

def reproduce(simulation, world, creature, signals):
    if signals[0] > 0.5 \
            and creature.state['energy'] > creature.config['creature'][creature.species]['min_energy_for_reproduction'] \
            and creature.state['age'] > creature.config['creature'][creature.species]['min_age_for_reproduction']:
        new_creature = creature.reproduce()

        # creating a creature can fail, so check this
        if new_creature is not None:
            simulation.add_creature(new_creature)

def eat_grass(simulation, world, creature, signals):
    if signals[0] > 0.5:
        row, col = creature.state['position'][0, 0], creature.state['position'][1, 0]
        if world.eat_grass(row, col, creature.config['creature'][creature.species]['grass_eat_speed']):
            creature.state['energy'] += creature.config['creature'][creature.species]['energy_from_grass']
        else:
            # eat dirt
            creature.state['energy'] += creature.config['creature'][creature.species]['energy_from_dirt']

def die(simulation, world, creature, signals):
    if signals[0] > 0.5:
        creature.state['energy'] = 0

def use_actuator(name, active, signals, simulation, world, creature):
    if active:
        globals()[name](simulation, world, creature, signals)
