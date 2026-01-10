import pygame
import sys
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from logger import log_state
from logger import log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

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

    Player.containers = (updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    asteroid_field = AsteroidField()

    ship = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    
    while True:
        log_state()
        updatable.update(dt)
        for current_asteroid in asteroids:
            if current_asteroid.collides_with(ship):
                log_event("player_hit")
                print("Game over!")
                sys.exit()
            for bullet in shots:
                ship.bullet_count = len(shots)
                if current_asteroid.collides_with(bullet):
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
