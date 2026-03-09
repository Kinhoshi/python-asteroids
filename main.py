import controls
import math
import pygame
import pygame_menu
import copy
import random
import sys
import time
from asteroid import Asteroid
from asteroidfield import AsteroidField
from config import GameOptions
from constants import BASE_WIDTH, BASE_HEIGHT, ASTEROID_MIN_RADIUS
from game_over_screen import game_over
from logger import log_state, log_event
from menu import run_main_menu, pause_menu
from octagonshape import OctagonShape
from player import Player
from player_lives import Lives
from shot import Shot
from stars import Star, StarField
from thrust_particles import Particle
from powerups import PowerUp_Box, Laser




pygame.init()
#pygame.mixer.init()
configurable_options = GameOptions()
SCREEN_WIDTH = configurable_options.SCREEN_WIDTH
SCREEN_HEIGHT = configurable_options.SCREEN_HEIGHT
pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)
if configurable_options.FULLSCREEN:
    try:
        flags = pygame.FULLSCREEN
        if hasattr(pygame, "SCALED"):
            flags |= pygame.SCALED
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags)
    except pygame.error:
        print("Fullscreen not supported, falling back to windowed mode")
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
else:
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
asteroids_theme = pygame_menu.themes.THEME_DARK.copy()
game_surface = pygame.Surface((BASE_WIDTH, BASE_HEIGHT))
current_game_state = ""
GAME_OVER = "GAME OVER"
PAUSED = "PAUSED"
PLAYING = "PLAYING"
MENU = "MENU"

def game_loop():
    global current_game_state
    global screen
    global configurable_options

    # This outer loop handles restarting the game.
    # When the game ends or is restarted, it will loop and re-initialize everything.
    while True:
        game_font = pygame.font.SysFont(None, 30)
        score = 0
        time_alive = 0
        danger_score_multiplier = 1
        asteroid_score_bonus = 0
        next_life_score = 25000
        score_text = game_font.render(f"Score: {score}", True, (255, 255, 255))
        score_rect = score_text.get_rect()
        score_rect.center = (BASE_WIDTH // 2, 10)
        life_text = game_font.render(f"Lives:", True, (255, 255, 255))
        life_rect = life_text.get_rect()
        life_rect.center = (40, 10)

        clock = pygame.time.Clock()
        dt = 0
        fps_color_1 = (0, 255, 0)
        fps_color_2 = (255, 255, 0)
        fps_color_3 = (255, 165, 0)
        fps_color_4 = (255, 0, 0)

        updatable = pygame.sprite.Group()
        drawable = pygame.sprite.Group()
        asteroids = pygame.sprite.Group()
        shots = pygame.sprite.Group()
        stars = pygame.sprite.Group()
        particles = pygame.sprite.Group()
        lives = pygame.sprite.Group()
        powerups = pygame.sprite.Group()

        Player.containers = (updatable, drawable)
        Lives.containers = (lives, updatable, drawable)
        Particle.containers = (particles, updatable, drawable)
        Shot.containers = (shots, updatable, drawable)
        Asteroid.containers = (asteroids, updatable, drawable)
        AsteroidField.containers = (updatable)
        
        # Create a copy of options for AsteroidField that enforces logical game size
        asteroid_field_options = copy.copy(configurable_options)
        asteroid_field_options.SCREEN_WIDTH = BASE_WIDTH
        asteroid_field_options.SCREEN_HEIGHT = BASE_HEIGHT
        asteroid_field = AsteroidField(asteroid_field_options)

        Star.containers = (stars, drawable)
        StarField(400, configurable_options)
        PowerUp_Box.containers = (powerups, updatable, drawable)

        ship = Player(BASE_WIDTH / 2, BASE_HEIGHT / 2, configurable_options)

        last_screen_width = configurable_options.SCREEN_WIDTH
        last_screen_height = configurable_options.SCREEN_HEIGHT

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
        game_is_running = True

        while game_is_running:
            # Calculate dt at the START of the frame to prevent spikes
            dt = clock.tick(60) / 1000
            #asteroid_explosions = random.choice(["explosion.wav", "explosion2.wav", "explosion3.wav", "explosion4.wav"])
            #asteroid_explosion_sound = pygame.mixer.Sound(f"data/{asteroid_explosions}")
            #asteroid_explosion_sound.set_volume(0.2)
            if dt > 0:
                fps = int(1 / dt)
            else:
                fps = 60
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    controls.handle_input_event(event, configurable_options.parser, configurable_options)
                    if event.key == configurable_options.CONTROLS_PAUSE:
                        current_game_state = PAUSED

            if len(lives) > ship.lives:
                life = lives.sprites()
                if life:
                    life.sort(key=lambda x: x.position.x)
                    life[-1].kill()

            if current_game_state == PLAYING:
                if configurable_options.SCREEN_WIDTH != last_screen_width or configurable_options.SCREEN_HEIGHT != last_screen_height:
                    last_screen_width = configurable_options.SCREEN_WIDTH
                    last_screen_height = configurable_options.SCREEN_HEIGHT
                    asteroid_field.kill()
                # Create a copy of options for AsteroidField that enforces logical game size
                asteroid_field_options = copy.copy(configurable_options)
                asteroid_field_options.SCREEN_WIDTH = BASE_WIDTH
                asteroid_field_options.SCREEN_HEIGHT = BASE_HEIGHT
                asteroid_field = AsteroidField(asteroid_field_options)

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
                    if bullet.time_alive >= 8 and not isinstance(bullet, Laser):
                        bullet.kill()
                ship.bullet_count = len(shots)
                for current_asteroid in asteroids:
                    if current_asteroid.position.distance_to((ship.position.x, ship.position.y)) < (current_asteroid.radius + ship.radius) * 1.5:
                        danger_score_multiplier = 3
                    elif current_asteroid.position.distance_to((ship.position.x, ship.position.y)) < (current_asteroid.radius + ship.radius) * 2:
                        danger_score_multiplier = 2
                    else:
                        danger_score_multiplier = 1
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
                            #asteroid_explosion_sound.play()
                            if current_asteroid.child:
                                if current_asteroid.radius == ASTEROID_MIN_RADIUS:
                                    asteroid_score_bonus = 100
                                elif current_asteroid.radius == ASTEROID_MIN_RADIUS * 2:
                                    asteroid_score_bonus = 50
                                else:
                                    asteroid_score_bonus = 0
                            if current_asteroid.color == "gold4":
                                score += (25 * danger_score_multiplier) + asteroid_score_bonus
                            else:
                                score += (1 * danger_score_multiplier) + asteroid_score_bonus
                            log_event("asteroid_shot")
                            current_asteroid.split()
                            # The laser is a continuous beam, so it shouldn't be destroyed on impact.
                            if not isinstance(bullet, Laser):
                                bullet.kill()
                screen.fill("black")
                game_surface.fill("black")
                for sprites in drawable:
                    sprites.draw(game_surface)
                game_surface.blit(score_text, score_rect)
                game_surface.blit(life_text, life_rect)
                if configurable_options.FPS_COUNTER:
                    if fps >= 50:
                        fps_color = fps_color_1
                    elif fps >= 40:
                        fps_color = fps_color_2
                    elif fps >= 20:
                        fps_color = fps_color_3
                    else:
                        fps_color = fps_color_4
                    fps_font = pygame.font.SysFont(None, 30)
                    fps_text = fps_font.render(f"FPS: {fps}", True, fps_color)
                    fps_rect = fps_text.get_rect()
                    fps_rect.topright = (BASE_WIDTH, 0)
                    game_surface.blit(fps_text, fps_rect)
                scaled_surface = pygame.transform.scale(game_surface, screen.get_size())
                score_text = game_font.render(f"Score: {score}", True, (255, 255, 255))
                screen.blit(scaled_surface, (0,0))
                pygame.display.flip()

            elif current_game_state == PAUSED:
                log_event("game_paused")
                pause_result = pause_menu(screen, game_surface, configurable_options, asteroids_theme, game_loop)
                if pause_result['quit_to_main']:
                    log_event("quit_game")
                    return  # Exit game_loop entirely to go to main menu

                elif pause_result['restart_game']:
                    log_event("game_restarted")
                    game_is_running = False # Exit inner loop to trigger a restart
                    continue

                else:  # User resumed from pause menu
                    current_game_state = PLAYING
                    log_event("game_resumed")
                    # Reset the clock after unpausing to avoid a large dt spike
                    clock.tick()

            elif current_game_state == GAME_OVER:
                log_event("game_over")
                # game_over returns True if user wants to quit the application
                if game_over(screen, configurable_options, score, time_alive):
                    return
                # Otherwise, the user wants to go to the main menu. Exit the game loop.
                return

def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}\nScreen width: {SCREEN_WIDTH}\nScreen height: {SCREEN_HEIGHT}")
    pygame.font.init()
    pygame.display.set_caption("py-Asteroids")
    while True:
        run_main_menu(screen, game_surface, configurable_options, asteroids_theme, game_loop)
        game_loop()

if __name__ == "__main__":
    main()