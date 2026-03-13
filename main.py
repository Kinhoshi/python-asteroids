import controls
import math
import pygame
import pygame_menu
import random
import sys
import time
from asteroid import Asteroid
from asteroidfield import AsteroidField
from config import GameOptions
from constants import BASE_WIDTH, BASE_HEIGHT, ASTEROID_MIN_RADIUS
from game_over_screen import game_over
from logger import log_state, log_event
from menu import run_main_menu, pause_menu, control_options_menu
from octagonshape import OctagonShape
from player import Player
from player_lives import Lives
from shot import Shot
from stars import Star, StarField
from thrust_particles import Particle
from powerups import PowerUp_Box, Laser




pygame.init()
pygame.mixer.init()
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

def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}\nScreen width: {SCREEN_WIDTH}\nScreen height: {SCREEN_HEIGHT}")
    pygame.font.init()
    pygame.display.set_caption("py-Asteroids")
    if any(str(getattr(configurable_options, n, "")) == "0" for n in ("CONTROLS_ACCELERATE","CONTROLS_ROTATE_LEFT","CONTROLS_ROTATE_RIGHT","CONTROLS_SHOOT")):
        control_options_menu(screen, game_surface, configurable_options, asteroids_theme, run_main_menu, run_loop=True)
    else:
        run_main_menu(screen, game_surface, configurable_options, asteroids_theme, game_loop)

def game_loop():
    while True:
        global current_game_state
        global screen
        global configurable_options

        game_font = pygame.font.SysFont(None, 30)
        ammo_font = pygame.font.SysFont(None, 25)
        score = 0
        time_alive = 0
        laser_timer = 5
        laser_timer_counter = 0
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
        asteroid_field = AsteroidField(configurable_options)
        Star.containers = (stars, drawable)
        StarField(400, configurable_options)
        PowerUp_Box.containers = (powerups, updatable, drawable)

        ship = Player(BASE_WIDTH / 2, BASE_HEIGHT / 2, configurable_options)

        ammo_text = ammo_font.render(f"Homing Missiles: {ship.ammo}", True, (255, 255, 255))
        ammo_rect = ammo_text.get_rect()
        ammo_rect.center = (75, 60)
        laser_text = ammo_font.render(f"Laser! Time Left: {laser_timer}", True, (255, 255, 255))
        laser_text_rect = laser_text.get_rect()
        laser_text_rect.center = (85, 60)
        
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
            asteroid_explosions = random.choice(["explosion.wav", "explosion2.wav", "explosion3.wav", "explosion4.wav"])
            asteroid_explosion_sound = pygame.mixer.Sound(f"assets/{asteroid_explosions}")
            asteroid_explosion_sound.set_volume(0.2)
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
                if ship.power != "laser" and laser_timer != 5:
                    laser_timer = 5
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
                    log_event("game_over")
                    ship.time_alive = 0
                    current_game_state = GAME_OVER
                for powerup in powerups:
                    if ship.collides_with(powerup):
                        if powerup.contents == "1up":
                            log_event("extra_life")
                            ship.lives += 1
                            life_shape = Lives(life_rect.right + 15 + ((ship.lives - 1) * 25), life_rect.centery + 15)
                            updatable.add(life_shape)
                            drawable.add(life_shape)
                            lives.add(life_shape)
                        elif powerup.contents == "homing":
                            log_event("homing_missiles_acquired")
                            ship.power = powerup.contents
                            ship.ammo += 15
                        elif powerup.contents == "laser":
                            log_event("laser_beam_acquired")
                            ship.power = powerup.contents
                            ship.laser_timer = 0
                            laser_timer = 5
                        powerup.kill()
                if ship.power == "homing":
                    ammo_text = ammo_font.render(f"Homing Missiles: {ship.ammo}", True, (255, 255, 255))

                if ship.power == "laser":
                    laser_timer_counter += dt
                    if laser_timer_counter >= 1:
                        laser_timer -= 1
                        laser_timer_counter = 0
                    laser_text = ammo_font.render(f"Laser! Time Left: {laser_timer}", True, (255, 255, 255))

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
                            asteroid_explosion_sound.play()
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
                if ship.power == "homing":
                    game_surface.blit(ammo_text, ammo_rect)
                if ship.power == "laser":
                    game_surface.blit(laser_text, laser_text_rect)
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
                dt = clock.tick(60) / 1000

            elif current_game_state == PAUSED:
                log_event("game_paused")
                pause_result = pause_menu(screen, game_surface, configurable_options, asteroids_theme, game_loop)
                if pause_result.get('quit_to_main'):
                    log_event("quit_game")
                    return  # Return to main menu
                elif pause_result.get('restart_game'):
                    log_event("restarting_game")
                    current_game_state = PLAYING
                    break
                else:
                    current_game_state = PLAYING
                    log_event("game_resumed")
                    clock.tick()

            elif current_game_state == GAME_OVER:
                log_event("game_over")
                game_over_result = game_over(screen, configurable_options, score, time_alive)
                if game_over_result["quit_to_menu"]:
                    current_game_state = MENU
                    clock.tick()
                    return
                if game_over_result["restart_game"]:
                    current_game_state = PLAYING
                    break

            elif current_game_state == MENU:
                if run_main_menu(screen, game_surface, configurable_options, asteroids_theme, game_loop):
                    return
                current_game_state = PLAYING
                clock.tick()

if __name__ == "__main__":
    main()