import pygame
import pygame_menu
import sys
import math
import time
from config import GameOptions
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from stars import Star, StarField
from menubg import MenuBackground
from menu import run_main_menu, pause_menu
from octagonshape import OctagonShape
from thrust_particles import Particle
from constants import BASE_WIDTH, BASE_HEIGHT



configurable_options = GameOptions()
SCREEN_WIDTH = configurable_options.SCREEN_WIDTH
SCREEN_HEIGHT = configurable_options.SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
asteroids_theme = pygame_menu.themes.THEME_DARK.copy()
game_surface = pygame.Surface((BASE_WIDTH, BASE_HEIGHT))


def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}\nScreen width: {SCREEN_WIDTH}\nScreen height: {SCREEN_HEIGHT}")
    pygame.init()
    pygame.display.set_caption("py-Asteroids")
    run_main_menu(screen, game_surface, configurable_options, asteroids_theme, game_loop)
    
   

def game_loop():
    global screen
    global configurable_options

    paused = False

    fps = pygame.time.Clock()
    dt = 0

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    stars = pygame.sprite.Group()
    particles = pygame.sprite.Group()


    Player.containers = (updatable, drawable)
    Particle.containers = (particles, updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    asteroid_field = AsteroidField(configurable_options)
    Star.containers = (stars, drawable)
    StarField(400, configurable_options)

    ship = Player(BASE_WIDTH / 2, BASE_HEIGHT / 2, configurable_options)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                paused = not paused
        if not paused:
            log_state()
            updatable.update(dt)
            ship.time_alive += dt
            for particle in particles:
                particle.time_alive += dt
                if particle.time_alive >= 0.1:
                    particle.kill()
            for bullet in shots:
                if bullet.friendly_fire and bullet.collides_with(ship):
                    log_event("player_hit")
                    bullet.kill()
                    ship.kill()
                    ship.lives -= 1
                    if ship.lives > 0:
                        ship.respawn()
                        updatable.add(ship)
                        drawable.add(ship)
                    else:
                        print(f"Game over! You survived for {math.floor(ship.time_alive)} seconds!")
                        print("Consider turning friendly fire off")
                        run_main_menu(screen, game_surface, configurable_options, asteroids_theme, game_loop)
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
                    ship.kill()
                    ship.lives -= 1
                    if ship.lives > 0:
                        ship.respawn()
                        updatable.add(ship)
                        drawable.add(ship)
                    else:
                        print(f"Game over! You survived for {math.floor(ship.time_alive)} seconds!")
                        run_main_menu(screen, game_surface, configurable_options, asteroids_theme, game_loop)
                for bullet in shots:
                    if bullet.collides_with(current_asteroid):
                        log_event("asteroid_shot")
                        current_asteroid.split()
                        bullet.kill()
        if paused:
            if pause_menu(screen, game_surface, configurable_options, asteroids_theme, game_loop):
                return
            Asteroid.containers = (asteroids, updatable, drawable)
            paused = not paused
            fps.tick(60)

        screen.fill("black")
        game_surface.fill("black")
        for sprites in drawable:
            sprites.draw(game_surface)
        scaled_surface = pygame.transform.scale(game_surface, screen.get_size())
        screen.blit(scaled_surface, (0,0))
        pygame.display.flip()
        dt = fps.tick(60) / 1000

if __name__ == "__main__":
    main()