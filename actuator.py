from world import World


def move(simulation, world, creature, signals):
    # TODO: think about how to move. direction + angle? use world/sim to limit movement
    # move left
    creature.state['position'] = [creature.state['position'][0] - signals[0] * 20,
                                  creature.state['position'][1]]

    # move right
    creature.state['position'] = [creature.state['position'][0] + signals[1] * 20,
                                  creature.state['position'][1]]

def reproduce(simulation, world, creature, signals):
    if signals[0] > 0.99:
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


def use_actuator(name, active, signals, simulation, world, creature):
    if active:
        globals()[name](simulation, world, creature, signals)
