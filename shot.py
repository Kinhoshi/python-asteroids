from constants import *
from circleshape import *

class Shot(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
#        self.color_timer = 0.0
#        self.colors = ["red", "orange", "yellow", "green", "blue", "indigo", "violet"]
#        self.color_index = 0
#        self.color = self.colors[self.color_index]
#        self.switch_color_interval = 0.2

    def draw(self, screen):
        center = self.position
        radius = self.radius
        pygame.draw.circle(screen, "white", center, radius, 0)

    def update(self, dt):
        super().update(dt)
        self.position += (self.velocity * dt)
#        self.color_timer += dt
#        if self.color_timer >= self.switch_color_interval:
#            self.color_timer = 0
#            self.color_index = (self.color_index + 1) % len(self.colors)
#            self.color = self.colors[self.color_index]