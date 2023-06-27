import random

import numpy as np
import pygame

import stopwatch
from actuator import use_actuator
from brain import Brain
from dna import DNA
from sensor import use_sensor


class Creature:
    def __init__(self, config, dna=None):
        self.config = config
        self.state = {
            # TODO: move position select to simulation
            'position': (random.randrange(0, config['world_parameters']['size']),
                         random.randrange(0, config['world_parameters']['size'])),
            'dna': DNA(config) if dna is None else dna,
            'energy': config['creature']['initial_energy'],
        }

        # add sensors from DNA
        self.state['sensors'] = self.state['dna'].get_sensors()
        self.state['actuators'] = self.state['dna'].get_actuators()
        self.state['properties'] = self.state['dna'].get_properties()

        # force ploidy in body
        if 'ploidy' not in self.state['properties']:
            self.state['properties']['ploidy'] = 1

        self.state['brain'] = Brain(config, self.state['dna'].brain)



    def draw_creature(self, screen):
        #screen.set_at((int(self.state['position'][0]), int(self.state['position'][1])), (255, 0, 0))
        creature_color = (0, 0, 0)
        if self.state['properties']['ploidy'] == 1:
            creature_color = (255, 0, 0)
        if self.state['properties']['ploidy'] == 2:
            creature_color = (0, 0, 255)
        pygame.draw.circle(screen, creature_color,
                           (int(self.state['position'][0]), int(self.state['position'][1])), min(10, max(1, self.state['energy'])))

    def update(self, simulation, world):
        stopwatch.start("sensors")
        inputs = self.get_sensors(simulation, world)
        stopwatch.stop("sensors")
        stopwatch.start("brain")
        outputs = self.use_brain(inputs)
        stopwatch.stop("brain")
        stopwatch.start("actuators")
        self.use_actuators(outputs, simulation, world)
        stopwatch.stop("actuators")

        self.state['energy'] -= self.config['creature']['energy_per_timestep']

        self.state['energy'] = min(self.state['energy'], self.config['creature']['max_energy'])

    def use_brain(self, inputs):
        # TODO: implement brain

        # dummy outputs 0-1
        outputs = self.state['brain'].full_forward_propagation(inputs)
        # for actuator in self.state['actuators']:
        #     outputs += [random.random() for _ in range(actuator[1])]
        return outputs

    def get_sensors(self, simulation, world):
        # update sensors
        inputs = {}

        # TODO: we could skip unused sensors, because the brains inits unknown sensors to zero
        for sensor in self.state['sensors']:
            value = use_sensor(sensor[0], sensor[1], sensor[2], simulation, world, self)
            inputs[sensor[0]] = np.reshape(value, (sensor[1], 1))

        # return sensordata as column vector for nn
        return inputs

    def use_actuators(self, outputs, simulation, world):
        output_start = 0
        for actuator in self.state['actuators']:
            use_actuator(actuator[0], actuator[2], outputs[actuator[0]], simulation, world, self)

    def reproduce(self, other=None, same_location=True, share_energy=True):
        new_dna = self.state['dna'].reproduce(other)
        new_creature = Creature(self.config, new_dna)

        if same_location:
            new_creature.state['position'] = self.state['position']

        if share_energy:
            new_creature.state['energy'] = self.state['energy'] = self.state['energy'] / 2

        return new_creature