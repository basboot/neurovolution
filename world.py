import pygame
import random

class World:

    EMPTY = 0
    GRASS = 1
    WATER = 2
    TREE = 3
    ROCK = 4
    SEA = 5
    # kadaver
    # luchtje

    def __init__(self, config, size=512):

        self.max_water_depth = config['world_parameters']['max_water_depth']
        self.grass_growing_speed = config['world_parameters']['grass_growing_speed']
        self.max_grass_length = config['world_parameters']['max_grass_length']
        self.max_terrain_height = config['world_parameters']['max_terrain_height']

        self.size = config['world_parameters']['size']
        self.grid = [[self.EMPTY for _ in range(size)] for _ in range(size)]
        self.grass_length = [[0 for _ in range(size)] for _ in range(size)]

        self.make_random_world()

    def make_random_world(self):
        for row in range(self.size):
            for col in range(self.size):
                if row < 0.1 * self.size or row > 0.9 * self.size:
                    tile_value = self.GRASS
                    self.grid[row][col] = tile_value
                    self.grass_length[row][col] = random.randint(1,self.max_grass_length)

    def eat_grass(self,row,col):
        if row > self.size - 1 or row < 0 or col > self.size - 1 or col < 0:
            return

        self.grass_length[row][col] -= 1
        if self.grass_length[row][col] <= 0:
            self.grid[row][col] = self.EMPTY



    def update(self):
        for row in range(self.size):
            for col in range(self.size):
                tile_value = self.grid[row][col]
                if tile_value == self.GRASS:
                    self.grass_length[row][col] = min(self.grass_length[row][col]+ self.grass_growing_speed, self.max_grass_length)



    def draw_world(self, screen):
        for row in range(self.size):
            for col in range(self.size):
                tile_value = self.grid[row][col]
                if tile_value == self.GRASS:
                    length = self.grass_length[row][col]
                    color = (0, 255 - length * 10 ,0)
                    screen.set_at((row,col), color)



    def give_information_about_location(self, row, col):
        if row > self.size - 1 or row < 0 or col > self.size - 1 or col < 0:
            return self.EMPTY

        tile_value = self.grid[row][col]
        return tile_value


