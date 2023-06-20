import pygame
import random

class World:

    EMPTY = 0
    GRASS = [1,2,3,4,5,6,7,8,9,10]  # 1..10 are possible grass lengths
    # WATER
    # TREE
    # ROCK

    def __init__(self, size=512):
        self.size = size
        self.grid = [[(self.EMPTY,(255,255,255)) for _ in range(size)] for _ in range(size)]

    def make_random_world(self):
        for row in range(self.size):
            for col in range(self.size):
                if self.size < row+col < 1.5 * self.size:
                    tile_value = random.choice(self.GRASS)
                    color = self.get_color(tile_value)
                    self.grid[row][col] = (tile_value, color)
    def update(self):
        pass

    def draw_world(self, screen):
        for row in range(self.size):
            for col in range(self.size):
                tile_value, color = self.grid[row][col]
                pygame.draw.rect(screen, color, (col, row, 1,1)) # rect is not necessary

    def give_information_about_location(self, row, col):
        tile_value, _ = self.grid[row][col]
        return tile_value

    def get_color(self, tile_value):
        if tile_value in self.GRASS :
            return (0, 255-4*tile_value, 0)  # Greenish color depending on length grass
        else:
            return (255, 255, 255)  # Default white color (if unknown tile type)
