import pygame

# player class
class TriangleShape(pygame.sprite.Sprite):
    def __init__(self, x, y):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()
        
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.rotation = 0


        def draw(self, screen):
            points = self.points
            # override
            pass

        def update(self, dt):
            SCREEN_WIDTH = pygame.display.get_surface().get_width()
            SCREEN_HEIGHT = pygame.display.get_surface().get_height()
            if self.position.x > SCREEN_WIDTH:
                self.position.x -= SCREEN_WIDTH
            if self.position.x < 0:
                self.position.x += SCREEN_WIDTH
            if self.position.y > SCREEN_HEIGHT:
                self.position.y -= SCREEN_HEIGHT
            if self.position.y < 0:
                self.position.y += SCREEN_HEIGHT
        
        def triangle(self):
            forward = pygame.Vector2(0, 1).rotate(self.rotation)
            right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
            a = self.position + forward * self.radius
            b = self.position - forward * self.radius - right
            c = self.position - forward * self.radius + right
        return [a, b, c]