from octagonshape import *
from constants import *
from logger import *
from config import GameOptions
import random


class Asteroid(OctagonShape):
    def __init__(self, x, y, radius, game_options):
        super().__init__(x, y, radius)
        self.rotation = 20
        self.rotation_speed = random.randint(0, ASTEROID_MAX_ROTATION_SPEED)
        self.color = "gray" + f"{random.randint(20, 100)}"
        self.game_options = game_options
        self.width = self.game_options.ASTEROID_PIXEL_WIDTH
        self.time_alive = 0 # used for background asteroids
        value = random.randint(0, 10)
        if value == 10:
            self.color = "gold4"
        self.local_vertices = self.octagon()

    def update(self, dt):
        super().update(dt)
        self.position += (self.velocity * dt)
        self.rotation += self.rotation_speed * dt

    def draw(self, screen):
        color = self.color
        points = self.get_world_vertices()
        pygame.draw.polygon(screen, color, points, self.width)

    def split(self):
        self.kill()
        old_radius = self.radius
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        log_event("asteroid_split")
        rand_angle = random.uniform(20, 50)
        first_angle = self.velocity.rotate(rand_angle)
        second_angle = self.velocity.rotate(-rand_angle)
        new_radius = old_radius - ASTEROID_MIN_RADIUS
        first_asteroid = Asteroid(self.position.x, self.position.y, new_radius, self.game_options)
        second_asteroid = Asteroid(self.position.x, self.position.y, new_radius, self.game_options)
        first_asteroid.velocity = first_angle * 1.2
        second_asteroid.velocity = second_angle * 1.2

    def resolve_asteroid_collision(self, other):
        delta = other.position - self.position
        if delta.length_squared() == 0:
            return
        normal = delta.normalize()
        min_distance = self.radius + other.radius
        current_distance = self.position.distance_to(other.position)
        penetration = min_distance - current_distance
        if penetration <= 0:
            return
        self.position -= normal * (penetration / 2)
        other.position += normal * (penetration / 2)
        self.velocity, other.velocity = other.velocity, self.velocity