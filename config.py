



class GameOptions:
    def __init__(self):
        self.SCREEN_WIDTH = getattr(self, "SCREEN_WIDTH", 800) 
        self.SCREEN_HEIGHT = getattr(self, "SCREEN_HEIGHT", 600)
        self.PLAYER_MAX_BULLETS_ON_SCREEN = getattr(self, "PLAYER_MAX_BULLETS_ON_SCREEN", 5)
        self.MAX_ASTEROIDS_ON_SCREEN = getattr(self, "MAX_ASTEROIDS_ON_SCREEN", 15)
        self.ASTEROID_KINDS = getattr(self, "ASTEROID_KINDS", 3)
        self.ASTEROID_PIXEL_WIDTH = getattr(self, "ASTEROID_PIXEL_WIDTH", 2)
        self.PLAYER_PIXEL_WIDTH = getattr(self, "PLAYER_PIXEL_WIDTH", 2)
        self.BULLET_PIXEL_WIDTH = getattr(self, "BULLET_PIXEL_WIDTH", 2)
        self.STAR_TWINKLE_EFFECT = getattr(self, "STAR_TWINKLE_EFFECT", True)
        self.BULLETS_COLLIDE_WITH_PLAYER = getattr(self, "BULLETS_COLLIDE_WITH_PLAYER", False)
        self.PLAYER_LIVES = getattr(self, "PLAYER_LIVES", 1)