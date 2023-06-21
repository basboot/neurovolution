import random

import numpy as np

from brain import create_random_brain

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
        self.brain = np.array(create_random_brain(self.get_brain_architecture()))

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

        self.body = np.array(self.body)


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

    def get_brain_architecture(self):
        nn_architecture = []
        n_inputs = 0
        for i in range(len(self.config['sensors']['functions'])):
            n_inputs += self.config['sensors']['functions'][i][1]

        n_outputs = 0
        for i in range(len(self.config['actuators']['functions'])):
            n_outputs += self.config['actuators']['functions'][i][1]

        input_dim = n_inputs

        # add hidden layers
        for layer_config in self.config['brain']['hidden_layers']:
            output_dim = layer_config[0]
            activation = layer_config[1]
            nn_architecture.append(
                {"input_dim": input_dim, "output_dim": output_dim, "activation": activation}
            )
            input_dim = output_dim

        # add output layer
        nn_architecture.append(
            {"input_dim": input_dim, "output_dim": n_outputs, "activation": self.config['brain']['output_activation']}
        )

        return nn_architecture

    def reproduce(self, other=None):
        brain = self.brain.copy() if other is None else (self.brain + other.brain) / 2
        body = self.body.copy() if other is None else (self.body + other.body) / 2

        if np.random.random() < self.config['mutation']['brain']['p']:
            brain = np.random.normal(brain, self.config['mutation']['brain']['sd'])

        if np.random.random() < self.config['mutation']['body']['p']:
            brain = np.random.normal(brain, self.config['mutation']['body']['sd'])

        return DNA(self.config, brain, body)




