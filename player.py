from circleshape import *
from constants import *
from config import GameOptions
from shot import *
import pygame

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.cooldown_timer = 0
        self.bullet_count = 0
        self.time_alive = 0
        self.width = getattr(self, "width", LINE_WIDTH)


    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def draw(self, screen):
        points = self.triangle()
        pygame.draw.polygon(screen, "white", points, self.width)

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
        configurable_options = GameOptions()
        PLAYER_MAX_BULLETS_ON_SCREEN = configurable_options.PLAYER_MAX_BULLETS_ON_SCREEN

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
        bullet = Shot(self.position.x, self.position.y, SHOT_RADIUS)
        bullet.velocity = pygame.Vector2(0, 1).rotate(self.rotation)
        bullet.velocity *= PLAYER_SHOOT_SPEED

    def collides_with(self, other):
        triangle_points = self.triangle()
        asteroid_pos = other.position
        inside = self.point_in_triangle(asteroid_pos, triangle_points[0], triangle_points[1], triangle_points[2])
        if inside:
            return True
        return False
        

    def point_in_triangle(self, p, a, b, c):
       ab = b - a
       ap = p - a

       bc = c - b
       bp = p - b

       ca = a - c
       cp = p - c

       cross1 = ab.cross(ap)
       cross2 = bc.cross(bp)
       cross3 = ca.cross(cp)

       if (cross1 > 0 and cross2 > 0 and cross3 > 0) or (cross1 < 0 and cross2 < 0 and cross3 < 0):
           return True
       return False