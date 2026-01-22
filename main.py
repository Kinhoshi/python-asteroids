import pygame
import sys
from constants import *
from logger import log_state
from logger import log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from stars import Star, StarField

def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}\nScreen width: {SCREEN_WIDTH}\nScreen height: {SCREEN_HEIGHT}")
    pygame.init()
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
        for current_asteroid in asteroids:
            asteroid_field.asteroid_count = len(asteroids)
            for secondary_asteroid in asteroids:
                if current_asteroid == secondary_asteroid:
                    continue
                if current_asteroid.collides_with(secondary_asteroid):
                    log_event("asteroid_collision")
            if ship.collides_with(current_asteroid):
                log_event("player_hit")
                print("Game over!")
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
        
        


if __name__ == "__main__":
    main()
