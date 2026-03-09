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
        self.game_options = game_options
        self.game_surface = pygame.Surface((BASE_WIDTH, BASE_HEIGHT))

        Asteroid.containers = (self.asteroids, self.updatable, self.drawable)
        Star.containers = (self.stars, self.drawable)
        AsteroidField.containers = (self.updatable)
        
        self.asteroid_field = AsteroidField(game_options)
        StarField(400, game_options)
        
        self.clock = pygame.time.Clock()
        self.dt = 0

    def draw(self, screen):
        self.dt = self.clock.tick(60) / 1000
        fps = int(self.clock.get_fps())
        fps_color_1 = (0, 255, 0)
        fps_color_2 = (255, 255, 0)
        fps_color_3 = (255, 165, 0)
        fps_color_4 = (255, 0, 0)

        if fps >= 50:
            fps_color = fps_color_1
        elif fps >= 40:
            fps_color = fps_color_2
        elif fps >= 20:
            fps_color = fps_color_3
        else:
            fps_color = fps_color_4

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
        if self.game_options.FPS_COUNTER:
            fps_font = pygame.font.SysFont(None, 30)
            fps_text = fps_font.render(f"FPS: {fps}", True, fps_color)
            fps_rect = fps_text.get_rect()
            fps_rect.topright = (BASE_WIDTH, 50)
            self.game_surface.blit(fps_text, fps_rect)
        scaled_surface = pygame.transform.scale(self.game_surface, screen.get_size())
        screen.blit(scaled_surface, (0, 0))