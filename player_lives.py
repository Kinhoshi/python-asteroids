import pygame
from triangleshape import TriangleShape
from constants import PLAYER_LENGTH
from config import GameOptions


class Lives(TriangleShape):
    def __init__(self, x, y):
        super().__init__(x, y)
        game_options = GameOptions()
        self.width = game_options.PLAYER_PIXEL_WIDTH
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        
    def draw(self, screen):
        self.points = self.get_world_vertices()
        pygame.draw.polygon(screen, "white", self.points, self.width)