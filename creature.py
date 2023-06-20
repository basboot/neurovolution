import random

import pygame

from dna import DNA


class Creature:
    def __init__(self, world_size=512):
        self.state = {
            'position': (random.randrange(0, world_size), random.randrange(0, world_size)),
            'dna': DNA()
        }

    def draw_creature(self, screen):
        screen.set_at(self.state['position'], (255, 0, 0))
        #pygame.draw.circle(screen, (255, 0, 0), self.state['position'], 10)

    def sense_act(self, sense):
        actions = None

        return actions