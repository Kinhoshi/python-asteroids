import pygame
import pygame_menu
import sys
import math
from constants import *
from logger import log_state
from logger import log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from stars import Star, StarField
from menubg import MenuBackground

def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}\nScreen width: {SCREEN_WIDTH}\nScreen height: {SCREEN_HEIGHT}")
    pygame.init()
    pygame.display.set_caption("py-Asteroids")
    main_menu()
    
   

def game_loop():
    fps = pygame.time.Clock()
    dt = 0
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

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
                ship.bullet_count = len(shots)
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
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    menu_background = MenuBackground()

    my_theme = pygame_menu.themes.THEME_DARK.copy()
    my_theme.background_color = (0, 0, 0, 0)
    
    menu = pygame_menu.Menu('py-Asteroids', SCREEN_WIDTH, SCREEN_HEIGHT, theme=my_theme)
    menu.add.button('Play', game_loop)
    menu.add.button('Options')
    menu.add.button('Quit', quit_game)
    menu.mainloop(screen, bgfun=menu_background.draw)

def quit_game():
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
    main_menu()