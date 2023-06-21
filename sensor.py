def heartbeat(simulation, world, creature):
    return [0] if simulation.simulation_step % creature.state['properties']['heartbeat'] > 0 else [1]

def use_sensor(name, n_values, active, simulation, world, creature):
    if active:
        return globals()[name](simulation, world, creature)
    else:
        return [0] * n_values
