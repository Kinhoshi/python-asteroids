import pygame
import random
from constants import *
from circleshape import *

class Star(CircleShape):
    def __init__(self, x, y, radius, game_options):
        super().__init__(x, y, radius)
        self.radius = radius
        self.twinkle = game_options.STAR_TWINKLE_EFFECT
        if self.twinkle:
            self.color = ["blue", "yellow", "red", "purple", "green", "white"]
        else: self.color = random.choice(["blue", "yellow", "red", "purple", "green", "white"])

    def draw(self, screen):
        center = self.position
        radius = self.radius
        if self.twinkle:
            pygame.draw.circle(screen, random.choice(self.color), center, radius, 0)
        else: pygame.draw.circle(screen, self.color, center, radius, 0)

    def update(self, dt):
        pass

class StarField:
    def __init__(self, num_stars, game_options):
        SCREEN_WIDTH = BASE_WIDTH
        SCREEN_HEIGHT = BASE_HEIGHT
        for _ in range(num_stars):
            for _ in range(10):
                x = random.randint(0, SCREEN_WIDTH)
                y = random.randint(0, SCREEN_HEIGHT)
                radius = random.randint(1, STAR_MAX_RADIUS)
                position = pygame.Vector2(x, y)
                
                if not any(star.position.distance_to(position) < (star.radius + radius) * 2 for star in Star.containers[0]):
                    Star(x, y, radius, game_options)
                    break
