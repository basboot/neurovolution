import random

import numpy as np

from brain import create_random_brain

class DNA:
    def __init__(self, config, species, brain=None, body=None):
        self.config = config
        self.species = species

        if brain is None:
            self.create_random_dna()
        else:
            self.brain = brain
            self.body = body

    def create_random_dna(self):
        # config for NN
        
        # collect sinput (sensors), hidden and output (actuators) layers
        layers = self.config['sensors'][self.species]['functions'] + \
                 self.config['brain'][self.species]['hidden_layers'] + \
                 self.config['actuators'][self.species]['functions']
        self.brain = np.array(create_random_brain(layers, self.config['brain'][self.species]['connections']))

        # physical properties
        self.body = []

        # put random value 0-1 for each sensor in dna
        for sensor in self.config['sensors'][self.species]['functions']:
            value = 1 if sensor[3] else random.random()
            self.body.append(value)

        # put random value 0-1 for each actuator in dna
        for actuator in self.config['actuators'][self.species]['functions']:
            value = 1 if actuator[3] else random.random()
            self.body.append(value)

        # put random values in configured range in dna
        for property in self.config['body'][self.species]['properties']:
            value = random.uniform(property[1], property[2])
            self.body.append(value)

        self.body = np.array(self.body)


    def get_sensors(self):
        sensors = []
        for i in range(len(self.config['sensors'][self.species]['functions'])):
            sensors.append((self.config['sensors'][self.species]['functions'][i][0],
                            self.config['sensors'][self.species]['functions'][i][1],
                            self.body[i] > 0.5 or self.config['sensors'][self.species]['functions'][i][3]))
        return sensors

    def get_actuators(self):
        actuators = []
        for i in range(len(self.config['actuators'][self.species]['functions'])):
            actuators.append((self.config['actuators'][self.species]['functions'][i][0],
                              self.config['actuators'][self.species]['functions'][i][1],
                              self.body[i + len(self.config['sensors'][self.species]['functions'])] > 0.5 \
                              or self.config['actuators'][self.species]['functions'][i][3]))
        return actuators

    def get_properties(self):
        properties = {}
        for i in range(len(self.config['body'][self.species]['properties'])):
            property = self.config['body'][self.species]['properties'][i]
            name = property[0]
            value = self.body[i + len(self.config['sensors'][self.species]['functions']) + \
                              len(self.config['actuators'][self.species]['functions'])]
            if property[3]:
                value = round(value)

            properties[name] = value

        return properties

    def reproduce(self, other=None):
        brain = self.brain.copy() if other is None else (self.brain + other.brain) / 2
        body = self.body.copy() if other is None else (self.body + other.body) / 2

        if np.random.random() < self.config['brain'][self.species]['mutation']['p']:
            brain = np.random.normal(brain, self.config['brain'][self.species]['mutation']['sd'])

        if np.random.random() < self.config['body'][self.species]['mutation']['p']:
            body = np.random.normal(body, self.config['body'][self.species]['mutation']['sd'])

        # clamp values between min and max after possible mutation
        for i in range(len(self.config['body'][self.species]['properties'])):
            property = self.config['body'][self.species]['properties'][i]
            min_value = property[1]
            max_value = property[2]

            value = self.body[i + len(self.config['sensors'][self.species]['functions']) + \
                              len(self.config['actuators'][self.species]['functions'])]
            value = max(min(value, max_value), min_value)
            body[i + len(self.config['sensors'][self.species]['functions']) + \
                      len(self.config['actuators'][self.species]['functions'])] = value

        return DNA(self.config, self.species, brain, body)




