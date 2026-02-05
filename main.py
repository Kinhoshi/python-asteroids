import pygame
import pygame_menu
import sys
import math
from constants import *
from config import GameOptions
from logger import log_state
from logger import log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from stars import Star, StarField
from menubg import MenuBackground
from octagonshape import OctagonShape


configurable_options = GameOptions()
SCREEN_WIDTH = configurable_options.SCREEN_WIDTH
SCREEN_HEIGHT = configurable_options.SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
asteroids_theme = pygame_menu.themes.THEME_DARK.copy()


def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}\nScreen width: {SCREEN_WIDTH}\nScreen height: {SCREEN_HEIGHT}")
    pygame.init()
    pygame.display.set_caption("py-Asteroids")
    main_menu()
    
   

def game_loop():
    global screen

    fps = pygame.time.Clock()
    dt = 0

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    stars = pygame.sprite.Group()


    Player.containers = (updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    asteroid_field = AsteroidField()
    Star.containers = (stars, drawable)
    StarField(400)

    ship = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    while True:
        log_state()
        updatable.update(dt)
        ship.time_alive += dt
        for bullet in shots:
            bullet.time_alive += dt
            if bullet.time_alive >= 8:
                bullet.kill()
        ship.bullet_count = len(shots)
        for current_asteroid in asteroids:
            asteroid_field.asteroid_count = len(asteroids)
            for secondary_asteroid in asteroids:
                if id(current_asteroid) <= id(secondary_asteroid):
                    continue
                if current_asteroid.collides_with(secondary_asteroid):
                        log_event("asteroid_collision")
                        if current_asteroid.radius == secondary_asteroid.radius:
                            current_asteroid.resolve_asteroid_collision(secondary_asteroid)
                        elif current_asteroid.radius < secondary_asteroid.radius:
                            current_asteroid.split()
                        else:
                            secondary_asteroid.split()
            if ship.collides_with(current_asteroid):
                log_event("player_hit")
                print(f"Game over! You survived for {math.floor(ship.time_alive)} seconds!")
                sys.exit()
            for bullet in shots:
                if bullet.collides_with(current_asteroid):
                    log_event("asteroid_shot")
                    current_asteroid.split()
                    bullet.kill()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        screen.fill("black")
        for sprites in drawable:
            sprites.draw(screen)
        pygame.display.flip()
        dt = fps.tick(60) / 1000

def main_menu():
    global asteroids_theme
    menu_background = MenuBackground()

    asteroids_theme.background_color = (0, 0, 0, 0)
    
    menu = pygame_menu.Menu('py-Asteroids', SCREEN_WIDTH, SCREEN_HEIGHT, theme=asteroids_theme)
    menu.add.button('Play', game_loop)
    menu.add.button('Options', options_menu)
    menu.add.button('Quit', quit_game)
    menu.mainloop(screen, bgfun=menu_background.draw)

def quit_game():
    pygame.quit()
    sys.exit()

def options_menu():
    global asteroids_theme

    menu_background = MenuBackground()
    asteroids_theme.background_color = (0, 0, 0, 0)
    menu = pygame_menu.Menu('Options', SCREEN_WIDTH, SCREEN_HEIGHT, theme=asteroids_theme)
    menu.add.button('Toggle Fullscreen', lambda: pygame.display.toggle_fullscreen())
    menu.add.button('Objects', objects_sub_menu)
    menu.add.button('Back', main_menu)
    menu.mainloop(screen, bgfun=menu_background.draw)

def objects_sub_menu():
    global asteroids_theme
    menu_background = MenuBackground()
    asteroids_theme.background_color = (0, 0, 0, 0)
    menu = pygame_menu.Menu('Object options', SCREEN_WIDTH, SCREEN_HEIGHT, theme=asteroids_theme)
    menu.add.selector('Asteroid Pixel Width', [('Classic', 2), ('Filled', 0)], onreturn=lambda item, value: set_attribute(Asteroid, 'width', value))
    menu.add.selector('Player Pixel Width', [('Classic', 2), ('Filled', 0)], onreturn=lambda item, value: set_attribute(Player, 'width', value))
    menu.add.selector('Bullet Pixel Width', [('Classic', 2), ('Filled', 0)], onreturn=lambda item, value: set_attribute(Shot, 'width', value))
    menu.add.selector('Player Max Bullets', [('Default', 5), ('Double', 10), ('Triple', 15)], onchange=lambda item, value: set_attribute(GameOptions, 'PLAYER_MAX_BULLETS_ON_SCREEN', value))
    menu.add.selector('Max Asteroids', [('Default', 15), ('Double', 30), ('Triple', 45)], onchange=lambda item, value: set_attribute(GameOptions, 'MAX_ASTEROIDS_ON_SCREEN', value))
    menu.add.selector('Asteroid Sizes', [('Default', 3), ('4', 4), ('5', 5)], onchange=lambda item, value: set_attribute(GameOptions, 'ASTEROID_KINDS', value))
    menu.add.selector('Star Twinkle Effect', [('On', True), ('Off', False)], onreturn=lambda item, value: set_attribute(Star, 'twinkle', value))
    menu.add.button('Back', options_menu)
    menu.mainloop(screen, bgfun=menu_background.draw)

def set_attribute(target, attr, value):
    setattr(target, attr, value)

if __name__ == "__main__":
    main()