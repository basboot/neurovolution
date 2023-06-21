
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

def use_actuator(name, active, signals, simulation, world, creature):
    if active:
        globals()[name](simulation, world, creature, signals)
