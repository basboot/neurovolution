from world import World


class Simulation:
    def __init__(self, debug=False):
        self.debug = debug

        self.world = World()


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