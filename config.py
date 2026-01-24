import pygame

class GameOptions:
    def __init__(self):
        self.SCREEN_WIDTH = getattr(self, "SCREEN_WIDTH", 1280)
        self.SCREEN_HEIGHT = getattr(self, "SCREEN_HEIGHT", 720)
        self.PLAYER_MAX_BULLETS_ON_SCREEN = getattr(self, "PLAYER_MAX_BULLETS_ON_SCREEN", 5)
        self.MAX_ASTEROIDS_ON_SCREEN = getattr(self, "MAX_ASTEROIDS_ON_SCREEN", 15)
        self.ASTEROID_KINDS = getattr(self, "ASTEROID_KINDS", 3)