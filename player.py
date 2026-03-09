from triangleshape import TriangleShape
from constants import *
from config import GameOptions
from shot import Shot
from powerups import HomingMissile, Laser
from asteroid import Asteroid
from thrust_particles import Particle
import pygame
import controls

class Player(TriangleShape):
    def __init__(self, x, y, game_options):
        super().__init__(x, y, length=PLAYER_LENGTH)
        self.velocity = pygame.Vector2(0, 0)
        self.rotation = 0
        self.cooldown_timer = 0
        self.bullet_count = 0
        self.time_alive = 0
        self.laser_timer = 0
        self.game_options = game_options
        self.width = game_options.PLAYER_PIXEL_WIDTH
        self.lives = game_options.PLAYER_LIVES
        self.angular_velocity = 0
        self.points = self.get_world_vertices()
        self.laser = None


    
    def draw(self, screen):
        super().draw(screen)
        pygame.draw.polygon(screen, "white", self.points, self.width)

    def update(self, dt):
        super().update(dt)
        self.points = self.get_world_vertices()
        self.cooldown_timer -= dt
        self.velocity *= 0.997
        self.angular_velocity *= 0.95
        self.position += self.velocity
        self.rotation += self.angular_velocity * dt
        PLAYER_MAX_BULLETS_ON_SCREEN = self.game_options.PLAYER_MAX_BULLETS_ON_SCREEN

        if controls.is_control_pressed(self.game_options.CONTROLS_ROTATE_LEFT) or controls.is_control_pressed(self.game_options.CONTROLS_ROTATE_LEFT_ALT):
            self.angular_velocity -= PLAYER_TURN_ACCELERATION
            mid_point = (self.points[0] + self.points[1]) / 2
            direction = (mid_point - self.position).normalize()
            for i in range(2):
                pos = mid_point + (direction * (i * PARTICLE_RADIUS * 1.5))
                Particle(pos.x, pos.y, PARTICLE_RADIUS)

        if controls.is_control_pressed(self.game_options.CONTROLS_ROTATE_RIGHT) or controls.is_control_pressed(self.game_options.CONTROLS_ROTATE_RIGHT_ALT):
            self.angular_velocity += PLAYER_TURN_ACCELERATION
            mid_point = (self.points[0] + self.points[2]) / 2
            direction = (mid_point - self.position).normalize()
            for i in range(2):
                pos = mid_point + (direction * (i * PARTICLE_RADIUS * 1.5))
                Particle(pos.x, pos.y, PARTICLE_RADIUS)

        if controls.is_control_pressed(self.game_options.CONTROLS_ACCELERATE) or controls.is_control_pressed(self.game_options.CONTROLS_ACCELERATE_ALT):
            self.velocity += pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_ACCELERATION_MAGNITUDE
            mid_point = (self.points[1] + self.points[2]) / 2
            backward_direction = pygame.Vector2(0, -1).rotate(self.rotation)
            pos = mid_point + backward_direction * PARTICLE_RADIUS
            Particle(pos.x, pos.y, PARTICLE_RADIUS)

        is_shooting = controls.is_control_pressed(self.game_options.CONTROLS_SHOOT) or controls.is_control_pressed(self.game_options.CONTROLS_SHOOT_ALT)

        if is_shooting and not self.laser:
            if self.cooldown_timer > 0 or self.bullet_count == PLAYER_MAX_BULLETS_ON_SCREEN:
                pass
            else:
                if controls.is_control_pressed(self.game_options.CONTROLS_SHOOT) or controls.is_control_pressed(self.game_options.CONTROLS_SHOOT_ALT):
                    self.shoot()
                    self.cooldown_timer = PLAYER_SHOOT_COOLDOWN_SECONDS
                    self.bullet_count += 1
        elif not is_shooting and self.laser:
            self.laser.kill()
            self.laser = None

        if self.laser:
            # Update laser's position and rotation to match the player
            tip = self.local_vertices[0].rotate(self.rotation) + self.position
            forward_direction = pygame.Vector2(0, 1).rotate(self.rotation)
            offset_vector = forward_direction * SHOT_RADIUS * 1.5
            self.laser.position = tip + offset_vector
            self.laser.rotation = self.rotation

        if self.velocity.length() >= PLAYER_MAX_SPEED:
            self.velocity = self.velocity.normalize() * PLAYER_MAX_SPEED

        if self.angular_velocity >= PLAYER_MAX_TURN_SPEED:
            self.angular_velocity = PLAYER_MAX_TURN_SPEED
        elif self.angular_velocity <= -PLAYER_MAX_TURN_SPEED:
            self.angular_velocity = -PLAYER_MAX_TURN_SPEED

    def shoot(self):
        #pygame.mixer.init()
        #bullet_sound = pygame.mixer.Sound("data/laserShoot.wav")
        #bullet_sound.set_volume(0.2)

        tip = self.local_vertices[0].rotate(self.rotation) + self.position
        forward_direction = pygame.Vector2(0, 1).rotate(self.rotation)
        offset_distance = SHOT_RADIUS * 1.5
        offset_vector = forward_direction * offset_distance
        bullet_pos = tip + offset_vector

        bullet = HomingMissile(bullet_pos.x, bullet_pos.y, self.game_options)
        #bullet_sound.play()
        bullet.velocity = pygame.Vector2(0, 1).rotate(self.rotation)
        bullet.velocity *= PLAYER_SHOOT_SPEED
        bullet.rotation = self.rotation

    def respawn(self):
        respawn_x = BASE_WIDTH / 2
        respawn_y = BASE_HEIGHT / 2
        self.position = pygame.Vector2(respawn_x, respawn_y)
        self.rotation = 0
        self.velocity = pygame.Vector2(0, 0)
        self.cooldown_timer = 0
        self.bullet_count = 0
        if self.laser:
            self.laser.kill()
            self.laser = None

        for asteroid in Asteroid.containers[0]:
            if asteroid.position.distance_to((respawn_x, respawn_y)) < (asteroid.radius + self.radius) * 2:
                asteroid.kill()