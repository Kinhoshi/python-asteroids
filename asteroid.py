from circleshape import *
from constants import *
from logger import *
import random


class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.color = None
        value = random.randint(0, 10)
        if value == 10:
            self.color == "gold4"
        self.color = "gray" + f"{random.randint(20, 100)}"

    def draw(self, screen):
        width = LINE_WIDTH
        center = self.position
        radius = self.radius
        pygame.draw.circle(screen, self.color, center, radius, width)

    def update(self, dt):
        super().update(dt)
        self.position += (self.velocity * dt)

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