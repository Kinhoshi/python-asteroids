import configparser
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(BASE_DIR, "config.ini")



class GameOptions:
    def __init__(self):
        self.parser = configparser.ConfigParser()
        self.parser.read(CONFIG_FILE)
        self.ASTEROID_KINDS = self.parser.getint("GameDifficulty", "MaxTypesOfAsteroids")
        self.ASTEROID_PIXEL_WIDTH = self.parser.getint("GameSettings", "AsteroidPixelWidth")
        self.BULLET_PIXEL_WIDTH = self.parser.getint("GameSettings", "BulletPixelWidth")
        self.BULLETS_COLLIDE_WITH_PLAYER = self.parser.getboolean("GameDifficulty", "BulletsKillPlayer")
        self.CONTROLS_ACCELERATE = self.parser["Controls"]["Accelerate"]
        self.CONTROLS_ACCELERATE_ALT = self.parser["Controls"]["AccelerateAlt"]
        self.CONTROLS_PAUSE = self.parser["Controls"]["Pause"]
        self.CONTROLS_PAUSE_ALT = self.parser["Controls"]["PauseAlt"]
        self.CONTROLS_ROTATE_LEFT = self.parser["Controls"]["RotateLeft"]
        self.CONTROLS_ROTATE_LEFT_ALT = self.parser["Controls"]["RotateLeftAlt"]
        self.CONTROLS_ROTATE_RIGHT = self.parser["Controls"]["RotateRight"]
        self.CONTROLS_ROTATE_RIGHT_ALT = self.parser["Controls"]["RotateRightAlt"]
        self.CONTROLS_SHOOT = self.parser["Controls"]["Shoot"]
        self.CONTROLS_SHOOT_ALT = self.parser["Controls"]["ShootAlt"]
        self.DIFFICULTY = self.parser["GameDifficulty"]["Difficulty"]
        self.MAX_ASTEROIDS_ON_SCREEN = self.parser.getint("GameDifficulty", "MaxAsteroidsOnScreen")
        self.PLAYER_LIVES = self.parser.getint("GameDifficulty", "StartingLives")
        self.PLAYER_MAX_BULLETS_ON_SCREEN = self.parser.getint("GameDifficulty", "MaxBulletsOnScreen")
        self.PLAYER_PIXEL_WIDTH = self.parser.getint("GameSettings", "PlayerPixelWidth")
        self.SCREEN_HEIGHT = self.parser.getint("VideoSettings", "height")
        self.SCREEN_WIDTH = self.parser.getint("VideoSettings", "width")
        self.STAR_TWINKLE_EFFECT = self.parser.getboolean("GameSettings", "StarTwinkleEffect")