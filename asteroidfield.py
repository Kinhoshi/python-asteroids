import pygame
import random
from asteroid import Asteroid
from player import Player
from config import GameOptions
from constants import *

class AsteroidField(pygame.sprite.Sprite):

    def __init__(self, game_options):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.spawn_timer = 0.0
        self.asteroid_count = 0
        self.game_options = game_options
        
        SCREEN_WIDTH = BASE_WIDTH
        SCREEN_HEIGHT = BASE_HEIGHT
        
        max_radius = ASTEROID_MIN_RADIUS * self.game_options.ASTEROID_KINDS
        
        self.edges = [
            [
                pygame.Vector2(1, 0),
                lambda y: pygame.Vector2(-max_radius, y * SCREEN_HEIGHT),
            ],
            [
                pygame.Vector2(-1, 0),
                lambda y: pygame.Vector2(
                    SCREEN_WIDTH + max_radius, y * SCREEN_HEIGHT
                ),
            ],
            [
                pygame.Vector2(0, 1),
                lambda x: pygame.Vector2(x * SCREEN_WIDTH, -max_radius),
            ],
            [
                pygame.Vector2(0, -1),
                lambda x: pygame.Vector2(
                    x * SCREEN_WIDTH, SCREEN_HEIGHT + max_radius
                ),
            ],
        ]

    def spawn(self, radius, position, velocity):
        for asteroid in Asteroid.containers[0]:
            if asteroid.position.distance_to(position) < (asteroid.radius + radius) * 2:
                return
        if hasattr(Player, "containers"):
            for player in Player.containers[0]:
                if isinstance(player, Player) and player.position.distance_to(position) < (player.radius + radius) * 2:
                    return
        asteroid = Asteroid(position.x, position.y, radius, self.game_options)
        asteroid.velocity = velocity

    def update(self, dt):
        self.spawn_timer += dt
        opts = GameOptions()
        if self.spawn_timer > ASTEROID_SPAWN_RATE_SECONDS and self.asteroid_count < self.game_options.MAX_ASTEROIDS_ON_SCREEN:
            self.spawn_timer = 0

            # spawn a new asteroid at a random edge
            edge = random.choice(self.edges)
            speed = random.randint(40, 100)
            velocity = edge[0] * speed
            velocity = velocity.rotate(random.randint(-30, 30))
            position = edge[1](random.uniform(0, 1)) 
            kind = random.randint(1, self.game_options.ASTEROID_KINDS)
            self.spawn(ASTEROID_MIN_RADIUS * kind, position, velocity)