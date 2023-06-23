import random

from world import World


def move(simulation, world, creature, signals):
    # TODO: think about how to move. direction + angle? use world/sim to limit movement
    # move left
    creature.state['position'] = [creature.state['position'][0] - signals[0] * 20,
                                  creature.state['position'][1]]

    # move right
    creature.state['position'] = [creature.state['position'][0] + signals[1] * 20,
                                  creature.state['position'][1]]

    # move up
    creature.state['position'] = [creature.state['position'][0],
                                  creature.state['position'][1] - signals[2] * 20]

    # move down
    creature.state['position'] = [creature.state['position'][0],
                                  creature.state['position'][1] + signals[3] * 20]

    # check world if move is possible
    creature.state['position'] = simulation.move(creature.state['position'])

def small_move(simulation, world, creature, signals):
    dx = random.choice([-1,0,1])
    dy = random.choice([-1,0,1])
    # make small move
    creature.state['position'] = [creature.state['position'][0] + dx ,
                                  creature.state['position'][1] + dy]

    # check world if move is possible
    creature.state['position'] = simulation.move(creature.state['position'])

def reproduce(simulation, world, creature, signals):
    if signals[0] > 0.99 and creature.state['energy'] > creature.config['creature']['min_energy_for_reproduction']:
        new_creature = creature.reproduce()
        simulation.add_creature(new_creature)

def eat_grass(simulation, world, creature, signals):
    if signals[0] > 0.5:
        row = int(creature.state['position'][0])
        col = int(creature.state['position'][1])
        information = world.give_information_about_location(row, col)
        if information == World.GRASS:
            world.eat_grass(row, col)
            creature.state['energy'] += creature.config['creature']['energy_from_grass']
        else:
            # eat dirt
            creature.state['energy'] += creature.config['creature']['energy_from_dirt']

def die(simulation, world, creature, signals):
    if signals[0] > 0.5:
        creature.state['energy'] = 0

def use_actuator(name, active, signals, simulation, world, creature):
    if active:
        globals()[name](simulation, world, creature, signals)
