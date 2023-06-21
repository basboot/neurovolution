import time

import tomli

from visualisation import Visualisation
from simulation import Simulation

time.sleep(10)

if __name__ == '__main__':

    with open("neurovolution.toml", mode="rb") as fp:
        config = tomli.load(fp)

    print(f"Start {config['application']['name']} {config['application']['version']}")

    simulation = Simulation(config)

    simulation.run(config['simulation']['max_iterations'])