import tomli

if __name__ == '__main__':

    with open("neurovolution.toml", mode="rb") as fp:
        config = tomli.load(fp)

    print(f"Start {config['application']['name']} {config['application']['version']}")

    # simulation loop
    simulation_step = 0

    while simulation_step < config['simulation']['max_iterations']:
        simulation_step += 1

        if config['application']['debug']:
            print(f"Simulation step: {simulation_step}")