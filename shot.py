from constants import *
from missileshape import MissileShape
import pygame

class Shot(MissileShape):
    def __init__(self, x, y, game_options):
        super().__init__(x, y)
        self.width = game_options.BULLET_PIXEL_WIDTH
        self.friendly_fire = game_options.BULLETS_COLLIDE_WITH_PLAYER
        self.time_alive = 0 # useful for higher resolutions
        self.color = "white"

    def draw(self, screen):
        points = self.get_world_vertices()
        pygame.draw.polygon(screen, self.color, points, self.width)
        
    def update(self, dt):
        super().update(dt)