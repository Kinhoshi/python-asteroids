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
from menu import run_main_menu, pause_menu
from octagonshape import OctagonShape
from thrust_particles import Particle
from constants import BASE_WIDTH, BASE_HEIGHT, ASTEROID_MIN_RADIUS
from game_over_screen import game_over
from player_lives import Lives





configurable_options = GameOptions()
SCREEN_WIDTH = configurable_options.SCREEN_WIDTH
SCREEN_HEIGHT = configurable_options.SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
asteroids_theme = pygame_menu.themes.THEME_DARK.copy()
game_surface = pygame.Surface((BASE_WIDTH, BASE_HEIGHT))
current_game_state = ""
GAME_OVER = "GAME OVER"
PAUSED = "PAUSED"
PLAYING = "PLAYING"
MENU = "MENU"



def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}\nScreen width: {SCREEN_WIDTH}\nScreen height: {SCREEN_HEIGHT}")
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption("py-Asteroids")
    run_main_menu(screen, game_surface, configurable_options, asteroids_theme, game_loop)
    
def game_loop():
    global current_game_state
    global screen
    global configurable_options

    game_font = pygame.font.SysFont(None, 30)
    score = 0
    time_alive = 0
    danger_score_multiplier = 1
    asteroid_score_bonus = 0
    next_life_score = 25000
    score_text = game_font.render(f"Score: {score}", True, (255, 255, 255))
    score_rect = score_text.get_rect()
    life_text = game_font.render(f"Lives:", True, (255, 255, 255))
    life_rect = life_text.get_rect()
    life_rect.center = (40, 10)

    fps = pygame.time.Clock()
    dt = 0

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    stars = pygame.sprite.Group()
    particles = pygame.sprite.Group()
    lives = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Lives.containers = (lives, updatable, drawable)
    Particle.containers = (particles, updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    asteroid_field = AsteroidField(configurable_options)
    Star.containers = (stars, drawable)
    StarField(400, configurable_options)

    ship = Player(BASE_WIDTH / 2, BASE_HEIGHT / 2, configurable_options)

    life_shape_pos_x = 25
    for i in range(0, ship.lives):
        if i == 0:
            life_shape = Lives(life_rect.right + 15, life_rect.centery + 15)
        if i > 0:
            life_shape = Lives(life_rect.right + 15 + life_shape_pos_x, life_rect.centery + 15)
            life_shape_pos_x += 25
        updatable.add(life_shape)
        drawable.add(life_shape)


    current_game_state = PLAYING

    while True:
        score_rect.center = (pygame.display.Info().current_w // 2, 10)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    current_game_state = PAUSED

        if len(lives) > ship.lives:
            life = lives.sprites()
            if life:
                life.sort(key=lambda x: x.position.x)
                life[-1].kill()

        if current_game_state == PLAYING:
            log_state()
            updatable.update(dt)
            ship.time_alive += dt
            time_alive = math.floor(ship.time_alive)
            if score >= next_life_score:
                ship.lives += 1
                life_shape = Lives(life_rect.right + 15 + ((ship.lives - 1) * 25), life_rect.centery + 15)
                updatable.add(life_shape)
                drawable.add(life_shape)
                lives.add(life_shape)
                next_life_score += 25000
            if ship.lives <= 0:
                ship.time_alive = 0
                current_game_state = GAME_OVER
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
                bullet.time_alive += dt
                if bullet.time_alive >= 8:
                    bullet.kill()
            ship.bullet_count = len(shots)
            for current_asteroid in asteroids:
                if current_asteroid.position.distance_to((ship.position.x, ship.position.y)) < (current_asteroid.radius + ship.radius) * 1.5:
                    danger_score_multiplier = 3
                elif current_asteroid.position.distance_to((ship.position.x, ship.position.y)) < (current_asteroid.radius + ship.radius) * 2:
                    danger_score_multiplier = 2
                else: danger_score_multiplier = 1
                asteroid_field.asteroid_count = len(asteroids)
                for secondary_asteroid in asteroids:
                    if id(current_asteroid) <= id(secondary_asteroid):
                        continue
                    if current_asteroid.collides_with(secondary_asteroid):
                            log_event("asteroid_collision")
                            current_asteroid.resolve_asteroid_collision(secondary_asteroid)
                if ship.collides_with(current_asteroid):
                    log_event("player_hit")
                    ship.kill()
                    ship.lives -= 1
                    if ship.lives > 0:
                        ship.respawn()
                        updatable.add(ship)
                        drawable.add(ship)
                for bullet in shots:
                    if bullet.collides_with(current_asteroid):
                        if current_asteroid.child:
                            if current_asteroid.radius == ASTEROID_MIN_RADIUS:
                                asteroid_score_bonus = 100
                            elif current_asteroid.radius == ASTEROID_MIN_RADIUS * 2:
                                asteroid_score_bonus = 50
                            else: asteroid_score_bonus = 0
                        if current_asteroid.color == "gold4":
                            score += (25 * danger_score_multiplier) + asteroid_score_bonus
                        else:
                            score += (1 * danger_score_multiplier) + asteroid_score_bonus
                        log_event("asteroid_shot")
                        current_asteroid.split()
                        bullet.kill()
            screen.fill("black")
            game_surface.fill("black")
            for sprites in drawable:
                sprites.draw(game_surface)
            scaled_surface = pygame.transform.scale(game_surface, screen.get_size())
            score_text = game_font.render(f"Score: {score}", True, (255, 255, 255))
            screen.blit(scaled_surface, (0,0))
            screen.blit(score_text, score_rect)
            screen.blit(life_text, life_rect)
            pygame.display.flip()
            dt = fps.tick(60) / 1000

        elif current_game_state == PAUSED:
            log_event("game_paused")
            if pause_menu(screen, game_surface, configurable_options, asteroids_theme, game_loop):
                return
            Asteroid.containers = (asteroids, updatable, drawable)
            current_game_state = PLAYING
            log_event("game_resumed")
            fps.tick(60)

        elif current_game_state == GAME_OVER:
            log_event("game_over")
            if game_over(screen, configurable_options, score, time_alive):
                return
            current_game_state = MENU
            fps.tick(60)


        elif current_game_state == MENU:
            if run_main_menu(screen, game_surface, configurable_options, asteroids_theme, game_loop):
                return
            current_game_state = PLAYING
            fps.tick(60)

if __name__ == "__main__":
    main()