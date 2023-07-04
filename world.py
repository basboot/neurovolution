import pygame
import random
import numpy as np

class World:

    EMPTY = 0
    GRASS = 1
    WATER = 2
    TREE = 3
    ROCK = 4
    SEA = 5
    BREEDING = 6
    RABBIT = 10
    # kadaver
    # luchtje

    def __init__(self, config, size=512):

        self.max_water_depth = config['world_parameters']['max_water_depth']
        self.grass_growing_speed = config['world_parameters']['grass_growing_speed']
        self.grass_eat_speed = config['world_parameters']['grass_eat_speed']
        self.max_grass_length = config['world_parameters']['max_grass_length']
        self.max_terrain_height = config['world_parameters']['max_terrain_height']
        self.max_temperature = config['world_parameters']['max_temperature']
        self.min_temperature = config['world_parameters']['min_temperature']
        self.delta_temperature = config['world_parameters']['delta_temperature']
        self.grass_density = config['world_parameters']['grass_density']
        self.size = size

        self.array_size = (self.size,self.size)
        self.grid = np.zeros(self.array_size)
        self.grass_length = np.zeros(self.array_size)
        self.animal_grid = np.zeros(self.array_size)

        self.make_random_world()

    def make_random_world(self):
        for row in range(self.size):
            for col in range(self.size):
                if random.random() < self.grass_density:
                    tile_value = self.GRASS
                    self.grid[row][col] = tile_value
                    self.grass_length[row][col] = self.max_grass_length
                else:
                    tile_value = self.EMPTY
                    self.grid[row][col] = tile_value


    def add_animal(self, position, animal):
        # space is occupied, so cannot add animal
        if self.animal_grid[int(position[0]), int(position[1])] > 0:
            return False
        else:
            self.animal_grid[int(position[0]), int(position[1])] = animal
            return True

    def remove_animal(self, position):
        if self.animal_grid[int(position[0]), int(position[1])] > 0:
            self.animal_grid[int(position[0]), int(position[1])] = 0
            return True
        else:
            return False

    def move_animal(self, from_position, to_position, animal):
        # check if animal is in this position
        if self.animal_grid[int(from_position[0]), int(from_position[1])] == animal:
            # check if animal can move to the other position
            if self.add_animal(to_position, animal):
                self.remove_animal(from_position)
                return True
            else:
                return False

    def eat_grass(self,row,col):
        if row > self.size - 1 or row < 0 or col > self.size - 1 or col < 0:
            return False

        if self.grass_length[row][col] == 0:
            return False

        self.grass_length[row][col] -= self.grass_eat_speed
        if self.grass_length[row][col] <= 0:
            self.grid[row][col] = self.EMPTY

        return True




    def update(self):
        #self.min_temperature -= self.delta_temperature
        #self.max_temperature += self.delta_temperature

        for row in range(self.size):
            for col in range(self.size):
                tile_value = self.grid[row][col]
                if tile_value == self.GRASS:
                    self.grass_length[row][col] = min(self.grass_length[row][col]+ self.grass_growing_speed, self.max_grass_length)
                if tile_value == self.EMPTY:
                    if random.random() < self.grass_density:
                        tile_value = self.GRASS
                        self.grid[row][col] = tile_value
                        self.grass_length[row][col] = self.max_grass_length




    def draw_world(self, screen):
        for row in range(self.size):
            for col in range(self.size):
                tile_value = self.grid[row][col]
                animal_value = self.animal_grid[row][col]
                if tile_value == self.GRASS:
                    length = self.grass_length[row][col]
                    color = (100,255,100)
                    screen.set_at((row,col), color)




    def give_information_about_location(self, row, col):
        # TODO: improve sides
        if row > self.size - 2 or row < 1 or col > self.size - 2 or col < 1:
            return np.zeros(9)

        info = self.grid[row-1:row+2,col-1:col+2].reshape(9)

        return info

    def give_information_about_animals(self, row, col):
        # TODO: improve sides
        if row > self.size - 2 or row < 1 or col > self.size - 2 or col < 1:
            return np.zeros(9)

        info = self.animal_grid[row - 1:row + 2, col - 1:col + 2].reshape(9)

        return info

    def give_information_about_temperature(self, row, col,time):
        # not used
        if row > self.size - 1 or row < 0 or col > self.size - 1 or col < 0:
            return -1

        temp = self.min_temperature + (self.max_temperature - self.min_temperature) * (row+col) / (2*self.size)
        return temp


