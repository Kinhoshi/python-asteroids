from octagonshape import *
from constants import *
from logger import *
import random


class Asteroid(OctagonShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.rotation = 20
        self.rotation_speed = random.randint(0, ASTEROID_MAX_ROTATION_SPEED)
        self.color = "gray" + f"{random.randint(20, 100)}"
        value = random.randint(0, 10)
        if value == 10:
            self.color = "gold4"
        self.local_vertices = self.octagon()

    def update(self, dt):
        super().update(dt)
        self.position += (self.velocity * dt)
        self.rotation += self.rotation_speed * dt

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
        first_asteroid = Asteroid(self.position.x, self.position.y, new_radius)
        second_asteroid = Asteroid(self.position.x, self.position.y, new_radius)
        first_asteroid.velocity = first_angle * 1.2
        second_asteroid.velocity = second_angle * 1.2