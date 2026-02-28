import pygame
import random
from circleshape import *

class Particle(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.time_alive = 0
        self.color = "azure" + f"{random.randint(1, 4)}"

    def draw(self, screen):
        center = self.position
        radius = self.radius
        pygame.draw.circle(screen, self.color, center, radius, 0)

    def update(self, dt):
        super().update(dt)
        self.position += (self.velocity * dt)