import pygame
class Visualisation:
    def __init__(self, scaling, size=(500, 500), framerate=30, interval=1):
        pygame.init()

        self.scaling = scaling

        self.win = pygame.display.set_mode((size[0] * self.scaling, size[1] * self.scaling))

        self.screen = pygame.Surface(size)

        self.clock = pygame.time.Clock()
        self.framerate = framerate
        self.frame = 0
        self.interval = interval

    def update(self, world, creatures, simulation):
        self.frame += 1
        if self.frame % self.interval > 0:
            return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        self.draw_world(world)

        for creature in creatures:
            creature.draw_creature(self.screen)

        simulation.draw_simulation(self.screen)

        self.win.blit(pygame.transform.scale(self.screen, self.win.get_rect().size), (0, 0))
        pygame.display.flip()
        self.clock.tick(self.framerate)

    def draw_world(self, world):
        self.screen.fill((255, 255, 255))
        world.draw_world(self.screen)