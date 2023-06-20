import pygame
class Visualisation:
    def __init__(self, size=(500, 500), framerate=30, interval=1):
        pygame.init()
        self.screen = pygame.display.set_mode(size)
        self.clock = pygame.time.Clock()
        self.framerate = framerate
        self.frame = 0
        self.interval = interval

    def update(self, world):
        self.frame += 1
        if self.frame % self.interval > 0:
            return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        self.draw_world(world)

        pygame.display.flip()
        self.clock.tick(self.framerate)

    def draw_world(self, world):
        self.screen.fill((255, 255, 255))
        world.draw_world(self.screen)