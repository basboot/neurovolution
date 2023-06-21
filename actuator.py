def move(simulation, world, creature, signals):
    # TODO: think about how to move. direction + angle? use world/sim to limit movement
    # move left
    creature.state['position'] = [int(creature.state['position'][0] + signals[0] * 2), int(creature.state['position'][1])]

    # move right
    creature.state['position'] = [int(creature.state['position'][0] + signals[1] * 2),
                                  int(creature.state['position'][1])]
def use_actuator(name, active, signals, simulation, world, creature):
    if active:
        globals()[name](simulation, world, creature, signals)
