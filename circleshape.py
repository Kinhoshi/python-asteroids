import pygame
from constants import BASE_WIDTH, BASE_HEIGHT, LINE_WIDTH

# class for star & particle objects
class CircleShape(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        # we will be using this later
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius
        self.color = "white"

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.position, self.radius, LINE_WIDTH)

    def update(self, dt):
        SCREEN_WIDTH = BASE_WIDTH
        SCREEN_HEIGHT = BASE_HEIGHT
        if self.position.x > SCREEN_WIDTH:
            self.position.x -= SCREEN_WIDTH
        if self.position.x < 0:
            self.position.x += SCREEN_WIDTH
        if self.position.y > SCREEN_HEIGHT:
            self.position.y -= SCREEN_HEIGHT
        if self.position.y < 0:
            self.position.y += SCREEN_HEIGHT

    def collides_with(self, other):
        if self.position.distance_to(other.position) <= self.radius + other.radius:
            return True
        return False