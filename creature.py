import random

import numpy as np
import pygame

from actuator import use_actuator
from brain import Brain
from dna import DNA
from sensor import use_sensor


class Creature:
    MAX_ENERGY = 100

    def __init__(self, config):
        self.state = {
            # TODO: move position select to simulation
            'position': (random.randrange(0, config['world_parameters']['size']),
                         random.randrange(0, config['world_parameters']['size'])),
            'dna': DNA(config),
            'energy': self.MAX_ENERGY,
        }

        # add sensors from DNA
        self.state['sensors'] = self.state['dna'].get_sensors()
        self.state['actuators'] = self.state['dna'].get_actuators()
        self.state['properties'] = self.state['dna'].get_properties()

        self.state['brain'] = Brain(self.state['dna'].get_brain_architecture(), self.state['dna'].brain)



    def draw_creature(self, screen):
        screen.set_at(self.state['position'], (255, 0, 0))
        #pygame.draw.circle(screen, (255, 0, 0), self.state['position'], 10)

    def update(self, simulation, world):
        inputs = self.get_sensors(simulation, world)
        outputs = self.use_brain(inputs)
        self.use_actuators(outputs, simulation, world)

    def use_brain(self, inputs):
        # TODO: implement brain

        # dummy outputs 0-1
        outputs = self.state['brain'].forward_propagation(inputs)
        # for actuator in self.state['actuators']:
        #     outputs += [random.random() for _ in range(actuator[1])]
        return outputs

    def get_sensors(self, simulation, world):
        # update sensors
        inputs = []

        for sensor in self.state['sensors']:
            inputs += use_sensor(sensor[0], sensor[1], sensor[2], simulation, world, self)

        # return sensordata as column vector for nn
        return np.reshape(inputs, (len(inputs), 1))

    def use_actuators(self, outputs, simulation, world):
        output_start = 0
        for actuator in self.state['actuators']:
            use_actuator(actuator[0], actuator[2], outputs[output_start:actuator[1]], simulation, world, self)