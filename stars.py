import pygame
import random
from constants import *
from circleshape import *

class Star(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.radius = radius
        self.color = ["blue", "yellow", "red", "purple", "green", "white"]

    def draw(self, screen):
        center = self.position
        radius = self.radius
        pygame.draw.circle(screen, random.choice(self.color), center, radius, 0)

    def update(self, dt):
        pass

class StarField:
    def __init__(self, num_stars):
        for _ in range(num_stars):
            for _ in range(10):
                x = random.randint(0, SCREEN_WIDTH)
                y = random.randint(0, SCREEN_HEIGHT)
                radius = random.randint(1, STAR_MAX_RADIUS)
                position = pygame.Vector2(x, y)
                
                if not any(star.position.distance_to(position) < star.radius + radius for star in Star.containers[0]):
                    Star(x, y, radius)
                    break
