import pygame
from constants import *
from asteroid import Asteroid
from asteroidfield import AsteroidField
from stars import Star, StarField

class MenuBackground:
    def __init__(self, game_options):
        self.updatable = pygame.sprite.Group()
        self.drawable = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()
        self.game_surface = pygame.Surface((BASE_WIDTH, BASE_HEIGHT))

        Asteroid.containers = (self.asteroids, self.updatable, self.drawable)
        Star.containers = (self.stars, self.drawable)
        AsteroidField.containers = (self.updatable)
        
        self.asteroid_field = AsteroidField(game_options)
        StarField(400, game_options)
        
        self.clock = pygame.time.Clock()
        self.dt = 0

    def draw(self, screen):
        self.dt = self.clock.tick(0) / 1000

        self.updatable.update(self.dt)
        for current_asteroid in self.asteroids:
            current_asteroid.time_alive += self.dt
            if current_asteroid.time_alive >= 15:
                    current_asteroid.split()
                    current_asteroid.time_alive = 0
            self.asteroid_field.asteroid_count = len(self.asteroids)
            for secondary_asteroid in self.asteroids:
                if id(current_asteroid) <= id(secondary_asteroid):
                    continue
                if current_asteroid.collides_with(secondary_asteroid):
                    current_asteroid.resolve_asteroid_collision(secondary_asteroid)
        screen.fill("black")
        self.game_surface.fill("black")
        for sprites in self.drawable:
            sprites.draw(self.game_surface)
        scaled_surface = pygame.transform.scale(self.game_surface, screen.get_size())
        screen.blit(scaled_surface, (0, 0))