from creature import Creature
from visualisation import Visualisation
from world import World


class Simulation:
    def __init__(self, config):
        self.debug = config['application']['debug']
        self.config = config

        self.world = World(config)

        self.visualisation = Visualisation(size=config['visualisation']['size'],
                                  framerate=config['visualisation']['framerate'],
                                  interval=config['visualisation']['interval']) \
        if config['visualisation']['on'] else None

        self.creatures = [Creature(config) for _ in range(config['simulation']['n_creatures'])]
        self.born_creatures = []
        self.dead_creatures = []
        self.simulation_step = 0

    def run(self, max_iterations):
        # simulation loop


        # TODO: populate world

        while self.simulation_step <max_iterations:
            self.simulation_step += 1

            if self.debug:
                print(f"Simulation step: {self.simulation_step}")

            self.world.update()

            for creature in self.creatures:
                creature.update(self, self.world)
                if creature.state['energy'] < 0:
                    self.dead_creatures.append(creature)

            # add new creatues
            self.creatures += self.born_creatures
            print(f"{len(self.born_creatures)} born")
            self.born_creatures = []

            # remove old creatures
            for creature in self.dead_creatures:
                self.creatures.remove(creature)
            self.dead_creatures = []

            # cleanup if there are more creatures than allowed
            if len(self.creatures) > self.config['simulation']['max_creatures']:
                self.creatures = self.creatures[0:self.config['simulation']['max_creatures']]

            # prevent extinction
            while len(self.creatures) < self.config['simulation']['min_creatures']:
                self.creatures.append(Creature(self.config))

            # show
            if self.visualisation is not None:
                self.visualisation.update(self.world, self.creatures)

            print(f"{len(self.creatures)} creatures")

    def add_creature(self, creature):
        self.born_creatures.append(creature)