from constants import *
from circleshape import *

class Shot(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.width = getattr(self, "width", LINE_WIDTH)
        self.time_alive = 0 # useful for higher resolutions


    def draw(self, screen):
        center = self.position
        radius = self.radius
        pygame.draw.circle(screen, "white", center, radius, self.width)

    def update(self, dt):
        super().update(dt)
        self.position += (self.velocity * dt)