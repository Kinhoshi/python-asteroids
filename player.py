from triangleshape import *
from constants import *
from config import GameOptions
from shot import *
from asteroid import Asteroid
from thrust_particles import Particle
import pygame

class Player(TriangleShape):
    def __init__(self, x, y, game_options):
        super().__init__(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.rotation = 0
        self.cooldown_timer = 0
        self.bullet_count = 0
        self.time_alive = 0
        self.game_options = game_options
        self.width = game_options.PLAYER_PIXEL_WIDTH
        self.lives = game_options.PLAYER_LIVES
        self.angular_velocity = 0


    
    def draw(self, screen):
        super().draw(screen)
        pygame.draw.polygon(screen, "white", self.points, self.width)

    def update(self, dt):
        super().update(dt)
        self.cooldown_timer -= dt
        self.velocity *= 0.99
        self.angular_velocity *= 0.9
        self.position += self.velocity
        self.rotation += self.angular_velocity * dt
        keys = pygame.key.get_pressed()
        PLAYER_MAX_BULLETS_ON_SCREEN = self.game_options.PLAYER_MAX_BULLETS_ON_SCREEN

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.angular_velocity -= PLAYER_TURN_ACCELERATION


        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.angular_velocity += PLAYER_TURN_ACCELERATION

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.velocity += pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_ACCELERATION_MAGNITUDE
            mid_point_x = (self.points[1].x + self.points[2].x) / 2
            mid_point_y = (self.points[1].y + self.points[2].y) / 2
            particle = Particle(mid_point_x, mid_point_y, PARTICLE_RADIUS)

        if self.cooldown_timer > 0 or self.bullet_count == PLAYER_MAX_BULLETS_ON_SCREEN:
            pass
        else:
            if pygame.KEYDOWN and keys[pygame.K_SPACE]:
                self.shoot()
                self.cooldown_timer = PLAYER_SHOOT_COOLDOWN_SECONDS
                self.bullet_count += 1

        if self.velocity.length() >= PLAYER_MAX_SPEED:
            self.velocity = self.velocity.normalize() * PLAYER_MAX_SPEED

        if self.angular_velocity >= PLAYER_MAX_TURN_SPEED:
            self.angular_velocity = PLAYER_MAX_TURN_SPEED

    def shoot(self):
        tip = self.local_vertices[0].rotate(self.rotation) + self.position
        
        forward_direction = pygame.Vector2(0, 1).rotate(self.rotation)
        offset_distance = SHOT_RADIUS * 1.5
        offset_vector = forward_direction * offset_distance
        
        bullet_pos = tip + offset_vector

        bullet = Shot(bullet_pos.x, bullet_pos.y, SHOT_RADIUS, self.game_options)
        bullet.velocity = pygame.Vector2(0, 1).rotate(self.rotation)
        bullet.velocity *= PLAYER_SHOOT_SPEED

    def respawn(self):
        respawn_x = BASE_WIDTH / 2
        respawn_y = BASE_HEIGHT / 2
        self.position = pygame.Vector2(respawn_x, respawn_y)
        self.rotation = 0
        self.velocity = pygame.Vector2(0, 0)
        self.cooldown_timer = 0
        self.bullet_count = 0

        for asteroid in Asteroid.containers[0]:
            if asteroid.position.distance_to((respawn_x, respawn_y)) < (asteroid.radius + self.radius) * 2:
                asteroid.kill()