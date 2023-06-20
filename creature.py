class Creature:
    def __init__(self):
        self.state = {
            'position': (0, 0)
        }

    def sense_act(self, sense):
        actions = None

        return actions