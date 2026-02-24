import pygame
import sys
import os
import json
from menubg import MenuBackground
from constants import BASE_WIDTH, BASE_HEIGHT, LINE_WIDTH
from menu import run_main_menu

def game_over(screen, game_options, score, time):
    background = MenuBackground(game_options)
    friendly_fire = game_options.BULLETS_COLLIDE_WITH_PLAYER
    flicker_timer = 0
    flicker_draw = True
    white_text = (255, 255, 255)
    running = True
    score += (time * 100)
    final_score = score
    player_name = ""
    input_text = ""
    input_active = True
    time_converted = time_converter(time)
    menu_option_index = 0
    high_score_list = None
    score_dict = {}

    try:
        with open("high_scores.json", "r") as f:
            high_score_list = json.load(f)
        if len(high_score_list) == 0:
            high_score_list = []

    except FileNotFoundError:
        open("high_scores.json", "w").write("[]")

    while running:
        high_score_font = pygame.font.SysFont(None, 40)
        if len(high_score_list) < 10:
            high_score_input = high_score_font.render(input_text, True, white_text)
            high_score_input_rect = high_score_input.get_rect()
            high_score_input_rect.center = (pygame.display.Info().current_w // 2, pygame.display.Info().current_h // 2 + 350)
        if len(high_score_list) == 10 and final_score > high_score_list[9]["score"]:
            high_score_input = high_score_font.render(input_text, True, white_text)
            high_score_input_rect = high_score_input.get_rect()
            high_score_input_rect.center = (pygame.display.Info().current_w // 2, pygame.display.Info().current_h // 2 + 350)
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
        high_score_text = score_font.render("High Scores", True, white_text)
        high_score_rect = high_score_text.get_rect()
        high_score_rect.center = (80, 15)
        menu_option_rects = [return_to_menu_rect, quit_rect, high_score_input_rect]
        selected_POS = menu_option_rects[menu_option_index]
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
                    menu_option_index -= 1
                    if menu_option_index <= 0:
                        menu_option_index = 0
                    selected_POS = menu_option_rects[menu_option_index]
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    menu_option_index += 1
                    if menu_option_index >= len(menu_option_rects):
                        menu_option_index = len(menu_option_rects) - 1
                    selected_POS = menu_option_rects[menu_option_index]
                if event.key == pygame.K_RETURN:
                    if selected_POS == quit_rect:
                        pygame.quit()
                        sys.exit()
                    elif selected_POS == return_to_menu_rect:
                        return True
                    elif selected_POS == high_score_input_rect:
                        input_active = False
                        player_name = input_text
                        score_dict = {
                            "name": player_name,
                            "score": final_score, # Store score as an integer
                            "time": time_converted,
                            "friendly_fire": str(friendly_fire)
                        }

                        # Check if the player's score qualifies for the high score list
                        is_high_score = False
                        if len(high_score_list) < 10:
                            is_high_score = True
                        # Compare the new score (int) with the lowest score in the list (converted to int)
                        elif high_score_list and final_score > int(high_score_list[-1]["score"]):
                            is_high_score = True

                        if is_high_score:
                            high_score_list.append(score_dict)
                            high_score_list.sort(key=lambda x: int(x["score"]), reverse=True)
                            if len(high_score_list) > 10:
                                high_score_list.pop()
                            
                            with open("high_scores.json", "w") as f:
                                json.dump(high_score_list, f)

                if selected_POS == high_score_input_rect and input_active:
                    if event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    elif len(input_text) < 8:
                        input_text += event.unicode

        high_scores_text = []
        line_y_pos = 20
        for scores in high_score_list:
            high_scores_text.append(f"{scores['name']} - {scores['score']} - {scores['time']}")
        for lines in high_scores_text:
            line_font = pygame.font.SysFont(None, 30)
            line_text = line_font.render(lines, True, white_text)
            line_y_pos += 20
            line_rect = line_text.get_rect()
            line_rect.left = (0)
            line_rect.top = line_y_pos
            screen.blit(line_text, line_rect)   

        screen.blit(game_over_text, game_over_rect)
        screen.blit(score_text, score_rect)
        screen.blit(time_text, time_rect)
        screen.blit(return_to_menu_text, return_to_menu_rect)
        screen.blit(quit_text, quit_rect)
        screen.blit(high_score_input, high_score_input_rect)
        screen.blit(high_score_text, high_score_rect)
        

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