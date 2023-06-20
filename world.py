import pygame
import random

class World:

    EMPTY = 0
    GRASS = [1,2,3,4,5,6,7,8,9,10]  # 1..10 are possible grass lengths
    WATER = [11,12,13,14,15,16,17,18,19,20] # 11 is shallow, 20 is deep
    # TREE
    ROCK = [31,32,33,34,35,36,37,38,39,40] # 31 is low, 40 is high

    def __init__(self, config, size=512):

        self.max_water_depth = config['world_parameters']['max_water_depth']
        self.grass_growing_speed = config['world_parameters']['grass_growing_speed']
        self.max_terrain_height = config['world_parameters']['max_terrain_height']

        self.size = config['world_parameters']['size']
        self.grid = [[(self.EMPTY,self.get_color(self.EMPTY)) for _ in range(size)] for _ in range(size)]
        self.make_random_world()

    def make_random_world(self):
        for row in range(self.size):
            for col in range(self.size):
                if 0.5 * self.size < row+col < 1.5 * self.size:
                    tile_value = random.choice(self.GRASS)
                    color = self.get_color(tile_value)
                    self.grid[row][col] = (tile_value, color)
                elif 0.3 * self.size < row+col < 0.5 * self.size:
                    tile_value = random.choice(self.WATER)
                    color = self.get_color(tile_value)
                    self.grid[row][col] = (tile_value, color)
                elif 1.5 * self.size < row+col < 2 * self.size:
                    tile_value = random.choice(self.ROCK)
                    color = self.get_color(tile_value)
                    self.grid[row][col] = (tile_value, color)

    def update(self):
        for row in range(self.size):
            for col in range(self.size):
                tile_value, color = self.grid[row][col]
                if tile_value in self.GRASS:
                    new_tile_value = min(tile_value + 1, 10)
                    new_color = self.get_color(tile_value)
                    self.grid[row][col] = (new_tile_value, new_color)

    def draw_world(self, screen):
        for row in range(self.size):
            for col in range(self.size):
                tile_value, color = self.grid[row][col]
                pygame.draw.rect(screen, color, (col, row, 1,1)) # rect is not necessary

        # screen.fill((255,0,0), ((50,50), (1, 1))) better?

    def give_information_about_location(self, row, col):
        tile_value, _ = self.grid[row][col]
        return tile_value

    def get_color(self, tile_value):
        if tile_value in self.GRASS :
            return (0, 255 - 10 * tile_value, 0)  # Greenish color depending on length grass
        elif tile_value in self.WATER :
            return (0, 0, 255 - 10 * tile_value)  # Blueish color depending on water depth
        elif tile_value in self.ROCK:
            return (150, 75, 0 )  # brown for now
        else:
            return (255, 255, 255)  # Default white color (if unknown tile type)
