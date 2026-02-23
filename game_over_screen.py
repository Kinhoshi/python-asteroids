import pygame
import sys
from menubg import MenuBackground
from constants import BASE_WIDTH, BASE_HEIGHT, LINE_WIDTH
from menu import run_main_menu

def game_over(screen, game_options, score, time):
    background = MenuBackground(game_options)
    flicker_timer = 0
    flicker_draw = True
    white_text = (255, 255, 255)
    running = True
    score += (time * 100)
    input_text = "_______"
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
    quit_text = return_to_menu_font.render("Quit to Desktop", True, white_text)
    quit_rect = quit_text.get_rect()
    quit_rect.center = (pygame.display.Info().current_w // 2, pygame.display.Info().current_h // 2 + 275)
    high_score_input = score_font.render(input_text, True, white_text)
    high_score_input_rect = high_score_input.get_rect()
    high_score_input_rect.center = (pygame.display.Info().current_w // 2, pygame.display.Info().current_h // 2 + 350)
    selected_POS = return_to_menu_rect
    


    while running:
        dt = pygame.time.Clock().tick(60) / 1000
        background.draw(screen)
        flicker_timer += dt
        return_to_menu_button = pygame.draw.rect(screen, "gray8", return_to_menu_rect, 0)
        quit_button = pygame.draw.rect(screen, "gray8", quit_rect, 0)
        high_score_input_box = pygame.draw.rect(screen, "black", high_score_input_rect, 1)
        if flicker_timer >= 0.5:
            flicker_draw = not flicker_draw
            flicker_timer = 0
        if flicker_draw:
            selected_rect = pygame.draw.rect(screen, "blue", selected_POS, 5)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    selected_POS = return_to_menu_rect
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    selected_POS = quit_rect
                if selected_POS == quit_rect and event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        selected_POS = high_score_input_rect
                if selected_POS == high_score_input_rect and event.key == pygame.K_UP or event.key == pygame.K_w:
                        selected_POS = quit_rect
                if event.key == pygame.K_RETURN:
                    if selected_POS == quit_rect:
                        pygame.quit()
                        sys.exit()
                    elif selected_POS == return_to_menu_rect:
                        return True
                if event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else: input_text += event.unicode
            

                    

        screen.blit(game_over_text, game_over_rect)
        screen.blit(score_text, score_rect)
        screen.blit(time_text, time_rect)
        screen.blit(return_to_menu_text, return_to_menu_rect)
        screen.blit(quit_text, quit_rect)
        screen.blit(high_score_input, high_score_input_rect)
        

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