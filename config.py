



class GameOptions:
    def __init__(self):
        self.SCREEN_WIDTH = 800 
        self.SCREEN_HEIGHT = 600
        self.PLAYER_MAX_BULLETS_ON_SCREEN = 5
        self.MAX_ASTEROIDS_ON_SCREEN = 15
        self.ASTEROID_KINDS = 3
        self.ASTEROID_PIXEL_WIDTH = 2
        self.PLAYER_PIXEL_WIDTH = 2
        self.BULLET_PIXEL_WIDTH = 2
        self.STAR_TWINKLE_EFFECT = True
        self.BULLETS_COLLIDE_WITH_PLAYER = False
        self.PLAYER_LIVES = 3