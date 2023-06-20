from creature import Creature
from visualisation import Visualisation
from world import World


class Simulation:
    def __init__(self, config):
        self.debug = config['application']['debug']

        self.world = World(config)

        self.visualisation = Visualisation(size=config['visualisation']['size'],
                                  framerate=config['visualisation']['framerate'],
                                  interval=config['visualisation']['interval']) \
        if config['visualisation']['on'] else None

        self.creatures = [Creature() for _ in range(config['simulation']['n_creatures'])]

    def run(self, max_iterations):
        # simulation loop
        simulation_step = 0

        # TODO: populate world

        while simulation_step <max_iterations:
            simulation_step += 1

            if self.debug:
                print(f"Simulation step: {simulation_step}")

            self.world.update()

            # TODO: random creation

            # show
            if self.visualisation is not None:
                self.visualisation.update(self.world, self.creatures)