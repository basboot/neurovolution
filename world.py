from creature import Creature


class World:
    def __init__(self):
        # TODO: init map

        self.creatures = []

    def sense(self, position):
        return []

    def update(self):
        # update creatures TODO: is this the best location to update the creatures
        for creature in self.creatures:
            sense = self.sense(creature.state['position'])
            actions = creature.sense_act(sense)
            print(actions)

        # update world