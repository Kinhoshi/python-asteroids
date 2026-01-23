from constants import *
from circleshape import *

class Shot(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        center = self.position
        radius = self.radius
        pygame.draw.circle(screen, "white", center, radius, 0)

    def update(self, dt):
        super().update(dt)
        self.position += (self.velocity * dt)