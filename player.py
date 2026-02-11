from triangleshape import *
from constants import *
from config import GameOptions
from shot import *
from asteroid import Asteroid
import pygame

class Player(TriangleShape):
    def __init__(self, x, y, game_options):
        super().__init__(x, y)
        self.rotation = 0
        self.cooldown_timer = 0
        self.bullet_count = 0
        self.time_alive = 0
        self.game_options = game_options
        self.width = game_options.PLAYER_PIXEL_WIDTH
        self.lives = game_options.PLAYER_LIVES


    
    def draw(self, screen):
        super().draw(screen)
        pygame.draw.polygon(screen, "white", self.points, self.width)

    def move(self, dt):
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * dt
        self.position += rotated_with_speed_vector
    
    def rotate(self, dt):
        self.rotation += (PLAYER_TURN_SPEED * dt)

    def update(self, dt):
        super().update(dt)
        self.cooldown_timer -= dt
        keys = pygame.key.get_pressed()
        PLAYER_MAX_BULLETS_ON_SCREEN = self.game_options.PLAYER_MAX_BULLETS_ON_SCREEN

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.rotate(-dt)

        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.rotate(dt)

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.move(dt)
        
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.move(-dt)

        if self.cooldown_timer > 0 or self.bullet_count == PLAYER_MAX_BULLETS_ON_SCREEN:
            pass
        else:
            if pygame.KEYDOWN and keys[pygame.K_SPACE]:
                self.shoot()
                self.cooldown_timer = PLAYER_SHOOT_COOLDOWN_SECONDS
                self.bullet_count += 1

    def shoot(self):
        forward_direction = pygame.Vector2(0, 1).rotate(self.rotation)
        offset_distance = SHOT_RADIUS * 1.5
        offset_vector = forward_direction * offset_distance
        bullet_pos_x = self.points[0].x + offset_vector.x
        bullet_pos_y = self.points[0].y + offset_vector.y

        bullet = Shot(bullet_pos_x, bullet_pos_y, SHOT_RADIUS, self.game_options)
        bullet.velocity = pygame.Vector2(0, 1).rotate(self.rotation)
        bullet.velocity *= PLAYER_SHOOT_SPEED

    def respawn(self):
        respawn_x = self.game_options.SCREEN_WIDTH / 2
        respawn_y = self.game_options.SCREEN_HEIGHT / 2
        self.position = pygame.Vector2(respawn_x, respawn_y)
        self.rotation = 0
        self.velocity = pygame.Vector2(0, 0)
        self.cooldown_timer = 0
        self.bullet_count = 0

        for asteroid in Asteroid.containers[0]:
            if asteroid.position.distance_to((respawn_x, respawn_y)) < (asteroid.radius + self.radius) * 2:
                asteroid.kill()