import random

import numpy as np
import pygame

import stopwatch
from actuator import use_actuator
from brain import Brain
from dna import DNA
from sensor import use_sensor


class Creature:
    def __init__(self, config, world, creature_config, dna=None, position=None):
        self.name = creature_config[0]
        self.id = creature_config[1]
        self.color = creature_config[2]

        self.config = config
        self.world = world

        self.species = self.name

        if position is None:
            # find position in the world for this creature
            while True:
                position = np.random.random_integers(0, config['world_parameters']['size'] - 1, (2, 1))
                animal_added = world.add_animal(position, self.id)

                # break if an empty spot has been found
                if animal_added:
                    break
        else:
            assert world.add_animal(position, self.id), "New creature position not empty"

        self.state = {
            # TODO: move position select to simulation
            'position': position,
            'dna': DNA(config, species=self.species) if dna is None else dna,
            'energy': config['creature'][self.species]['initial_energy'],
            'age': 0
        }

        # add sensors from DNA
        self.state['sensors'] = self.state['dna'].get_sensors()
        self.state['actuators'] = self.state['dna'].get_actuators()
        self.state['properties'] = self.state['dna'].get_properties()

        # force ploidy in body
        if 'ploidy' not in self.state['properties']:
            self.state['properties']['ploidy'] = 1

        self.state['brain'] = Brain(config, self.state['dna'].brain, self.species)



    def draw_creature(self, screen):
        screen.set_at((self.state['position'][0, 0], self.state['position'][1, 0]), self.color)
        # creature_color = (0, 0, 0)
        # if self.state['properties']['ploidy'] == 1:
        #     creature_color = (255, 0, 0)
        # if self.state['properties']['ploidy'] == 2:
        #     creature_color = (0, 0, 255)
        # pygame.draw.circle(screen, creature_color,
        #                    (int(self.state['position'][0]), int(self.state['position'][1])), min(10, max(1, self.state['energy'])))

    def update(self, simulation, world):
        self.state['age'] += 1

        stopwatch.start("sensors")
        inputs = self.get_sensors(simulation, world)
        stopwatch.stop("sensors")
        stopwatch.start("brain")
        outputs = self.use_brain(inputs)
        stopwatch.stop("brain")
        stopwatch.start("actuators")
        self.use_actuators(outputs, simulation, world)
        stopwatch.stop("actuators")


        temp = world.give_information_about_temperature(self.state['position'][0],self.state['position'][1],0)
        factor = 1 if 5 < temp < 25 else 100
        self.state['energy'] -= self.config['creature'][self.species]['energy_per_timestep']*factor

        self.state['energy'] = min(self.state['energy'], self.config['creature'][self.species]['max_energy'])

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

    def reproduce(self, other=None):
        new_dna = self.state['dna'].reproduce(other)

        # choose position
        new_position = self.state['position'] + np.random.randint(-1, 2, (2, 1))

        # to see if the position is empty, we just try to put a test animal in the world
        if self.world.add_animal(new_position, self.id):
            # remove test animal
            self.world.remove_animal(new_position)
            # create real animal
            new_creature = Creature(self.config, self.world, [self.name, self.id, self.color], dna=new_dna, position=new_position)
            return new_creature
        else:
            # position not empty, reproduction fails
            return None