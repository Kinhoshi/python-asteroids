from octagonshape import *
from constants import *
from logger import *
from config import GameOptions
from powerups import PowerUp_Box
import random


class Asteroid(OctagonShape):
    def __init__(self, x, y, radius, game_options):
        super().__init__(x, y, radius)
        from circleshape import CircleShape
        self.rotation = 20
        self.rotation_speed = random.randint(0, ASTEROID_MAX_ROTATION_SPEED)
        self.color = "gray" + f"{random.randint(25, 100)}"
        self.game_options = game_options
        self.width = self.game_options.ASTEROID_PIXEL_WIDTH
        self.time_alive = 0 # used for background asteroids
        self.child = False # used for score multiplier
        self.powerup = random.randint(1, 50) == 10
        value = random.randint(1, 20)
        if value == 10:
            self.color = "gold4"
        self.local_vertices = self.octagon()

    def update(self, dt):
        super().update(dt)
        self.position += (self.velocity * dt)
        self.rotation += self.rotation_speed * dt
        if self.velocity.length() >= ASTEROID_MAX_SPEED:
            self.velocity = self.velocity.normalize() * ASTEROID_MAX_SPEED

    def draw(self, screen):
        points = self.get_world_vertices()
        pygame.draw.polygon(screen, self.color, points, self.width)

    def split(self):
        self.kill()
        if self.powerup:
            powerup = PowerUp_Box(self.position.x, self.position.y, 40, 40, self.game_options)

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
        first_asteroid.child = True
        second_asteroid.child = True
        if self.color == "gold4":
            first_asteroid.color = "gold4"
            second_asteroid.color = "gold4"

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
            
        m1 = self.radius ** 3
        m2 = other.radius ** 3
        total_mass = m1 + m2

        self.position -= normal * (penetration * (m2 / total_mass))
        other.position += normal * (penetration * (m1 / total_mass))

        v1 = self.velocity
        v2 = other.velocity
        dot_prod = (v1 - v2).dot(delta)

        if dot_prod > 0:
            dist_sq = current_distance ** 2
            collision_scale = dot_prod / dist_sq
            restitution = 0.6
            self.velocity -= (1 + restitution) * (m2 / total_mass) * collision_scale * delta
            other.velocity += (1 + restitution) * (m1 / total_mass) * collision_scale * delta