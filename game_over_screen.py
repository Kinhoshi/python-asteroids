import pygame
import sys
from menubg import MenuBackground
from constants import BASE_WIDTH, BASE_HEIGHT, LINE_WIDTH
from menu import run_main_menu

def game_over(screen, game_options, score, time):
    background = MenuBackground(game_options)
    white_text = (255, 255, 255)
    running = True
    score += (time * 100)
    time_converted = time_converter(time)
    game_over_font = pygame.font.SysFont(None, 100)
    game_over_text = game_over_font.render("GAME OVER", True, white_text)
    game_over_rect = game_over_text.get_rect()
    game_over_rect.center = (pygame.display.Info().current_w // 2, pygame.display.Info().current_h // 2)
    score_font = pygame.font.SysFont(None, 40)
    score_text = score_font.render(f"Score: {score}", True, white_text)
    score_rect = score_text.get_rect()
    score_rect.center = (pygame.display.Info().current_w // 2, pygame.display.Info().current_h // 2 + 75)
    time_font = score_font
    time_text = time_font.render(f"Time Survived: {time_converted}", True, white_text)
    time_rect = time_text.get_rect()
    time_rect.center = (pygame.display.Info().current_w // 2, pygame.display.Info().current_h // 2 + 125)
    return_to_menu_font = game_over_font
    return_to_menu_text = return_to_menu_font.render("Quit to Main Menu", True, white_text)
    return_to_menu_rect = return_to_menu_text.get_rect()
    return_to_menu_rect.center = (pygame.display.Info().current_w // 2, pygame.display.Info().current_h // 2 + 200)
    


    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
                pygame.quit()
                sys.exit()
        background.draw(screen)
        return_to_menu_button = pygame.draw.rect(screen, "gray8", return_to_menu_rect, 0)
        screen.blit(game_over_text, game_over_rect)
        screen.blit(score_text, score_rect)
        screen.blit(time_text, time_rect)
        screen.blit(return_to_menu_text, return_to_menu_rect)

        pygame.display.flip()

def time_converter(time):
    hours = time // 3600
    minutes = time // 60
    seconds = time % 60
    if time >= 3600:
        return f"{hours} hours, {minutes} minutes and {seconds} seconds" if hours > 1 else f"{hours} hour, {minutes} minutes and {seconds} seconds"
    elif time >= 60:
        return f"{minutes} minutes and {seconds} seconds" if minutes > 1 else f"{minutes} minute and {seconds} seconds"
    else:
        return f"{seconds} seconds" if seconds > 1 else f"{seconds} second"