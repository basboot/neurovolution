import tomli

from Visualisation import Visualisation
from simulation import Simulation

if __name__ == '__main__':

    with open("neurovolution.toml", mode="rb") as fp:
        config = tomli.load(fp)

    print(f"Start {config['application']['name']} {config['application']['version']}")

    visualisation = Visualisation(size=config['visualisation']['size'],
                                  framerate=config['visualisation']['framerate'],
                                  interval=config['visualisation']['interval']) \
        if config['visualisation']['on'] else None

    simulation = Simulation(debug=config['application']['debug'], visualisation=visualisation)
    simulation.run(config['simulation']['max_iterations'])