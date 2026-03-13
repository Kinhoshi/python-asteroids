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
        self.CONTROLS_ACCELERATE = self.parser.getint("Controls", "Accelerate")
        self.CONTROLS_ACCELERATE_ALT = self.parser.getint("Controls", "AccelerateAlt")
        self.MOUSE_AIM = self.parser.getboolean("GameSettings", "MouseAim")
        # 27 is the int value for the escape key in pygame
        self.CONTROLS_PAUSE = self.parser.getint("Controls", "Pause") if self.parser.getint("Controls", "Pause") != 0 else 27
        self.CONTROLS_PAUSE_ALT = self.parser.getint("Controls", "PauseAlt")
        self.CONTROLS_ROTATE_LEFT = self.parser.getint("Controls", "RotateLeft")
        self.CONTROLS_ROTATE_LEFT_ALT = self.parser.getint("Controls", "RotateLeftAlt")
        self.CONTROLS_ROTATE_RIGHT = self.parser.getint("Controls", "RotateRight")
        self.CONTROLS_ROTATE_RIGHT_ALT = self.parser.getint("Controls", "RotateRightAlt")
        self.CONTROLS_SHOOT = self.parser.getint("Controls", "Shoot")
        self.CONTROLS_SHOOT_ALT = self.parser.getint("Controls", "ShootAlt")
        self.DIFFICULTY = self.parser["GameDifficulty"]["Difficulty"]
        self.FPS_COUNTER = self.parser.getboolean("VideoSettings", "FPSCounter")
        self.FULLSCREEN = self.parser.getboolean("VideoSettings", "fullscreen")
        self.MAX_ASTEROIDS_ON_SCREEN = self.parser.getint("GameDifficulty", "MaxAsteroidsOnScreen")
        self.PLAYER_LIVES = self.parser.getint("GameDifficulty", "StartingLives")
        self.PLAYER_MAX_BULLETS_ON_SCREEN = self.parser.getint("GameDifficulty", "MaxBulletsOnScreen")
        self.PLAYER_PIXEL_WIDTH = self.parser.getint("GameSettings", "PlayerPixelWidth")
        self.SCREEN_HEIGHT = self.parser.getint("VideoSettings", "height")
        self.SCREEN_WIDTH = self.parser.getint("VideoSettings", "width")
        self.STAR_TWINKLE_EFFECT = self.parser.getboolean("GameSettings", "StarTwinkleEffect")