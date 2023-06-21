import random

from sensor import *


class DNA:
    def __init__(self, config, brain=None, body=None):
        self.config = config

        if brain is None:
            self.create_random_dna()
        else:
            self.brain = brain
            self.body = body

    def create_random_dna(self):
        # config for NN
        self.brain = []

        # physical properties
        self.body = []

        # put random value 0-1 for each sensor in dna
        for _ in self.config['sensors']['functions']:
            value = random.random()
            self.body.append(value)

        # put random value 0-1 for each actuator in dna
        for _ in self.config['actuators']['functions']:
            value = random.random()
            self.body.append(value)

        # put random values in configured range in dna
        for property in self.config['dna']['properties']:
            value = random.uniform(property[1], property[2])
            self.body.append(value)


    def get_sensors(self):
        sensors = []
        for i in range(len(self.config['sensors']['functions'])):
            sensors.append((self.config['sensors']['functions'][i][0],
                            self.config['sensors']['functions'][i][1],
                            self.body[i] > 0.5))
        return sensors

    def get_actuators(self):
        actuators = []
        for i in range(len(self.config['actuators']['functions'])):
            actuators.append((self.config['actuators']['functions'][i][0],
                              self.config['actuators']['functions'][i][1],
                              self.body[i + len(self.config['sensors']['functions'])] > 0.5))
        return actuators

    def get_properties(self):
        properties = {}
        for i in range(len(self.config['dna']['properties'])):
            property = self.config['dna']['properties'][i]
            name = property[0]
            value = self.body[i + len(self.config['sensors']['functions']) + len(self.config['actuators']['functions'])]
            if property[3]:
                value = round(value)

            properties[name] = value

        return properties




