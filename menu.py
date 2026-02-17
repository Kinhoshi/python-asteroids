import pygame
import pygame_menu
import sys
import weakref
from config import GameOptions
from menubg import MenuBackground

screen = None
configurable_options = None
asteroids_theme = None
SCREEN_WIDTH = 0
SCREEN_HEIGHT = 0
menus = weakref.WeakSet()

def run_main_menu(screen_obj, game_surface, game_options_obj, theme_obj, game_loop_func):
    global screen
    global configurable_options
    global asteroids_theme
    global SCREEN_WIDTH
    global SCREEN_HEIGHT

    screen = screen_obj
    surface = game_surface
    configurable_options = game_options_obj
    asteroids_theme = theme_obj
    SCREEN_WIDTH = configurable_options.SCREEN_WIDTH
    SCREEN_HEIGHT = configurable_options.SCREEN_HEIGHT

    def set_attribute_internal(target, attr, value):
        setattr(target, attr, value)

    def options_menu_internal():
        options_menu = pygame_menu.Menu('Options', SCREEN_WIDTH, SCREEN_HEIGHT, theme=asteroids_theme)
        menus.add(options_menu)
        options_menu.add.button('Difficulty Settings', difficulty_menu_internal())
        options_menu.add.button('Object Options', objects_sub_menu_internal())
        options_menu.add.button('Video Options', video_options())
        options_menu.add.button('Back', pygame_menu.events.BACK)
        return options_menu

    def objects_sub_menu_internal():
        asteroid_pixel_width = configurable_options.ASTEROID_PIXEL_WIDTH
        player_pixel_width = configurable_options.PLAYER_PIXEL_WIDTH
        bullet_pixel_width = configurable_options.BULLET_PIXEL_WIDTH
        star_twinkle_effect = configurable_options.STAR_TWINKLE_EFFECT
        
        objects_menu = pygame_menu.Menu('Object options', SCREEN_WIDTH, SCREEN_HEIGHT, theme=asteroids_theme)
        menus.add(objects_menu)
        objects_menu.add.selector('Asteroid Pixel Width', [('Classic', 2), ('Filled', 0)], default=0 if asteroid_pixel_width == 2 else 1, onchange=lambda item, value: set_attribute_internal(configurable_options, 'ASTEROID_PIXEL_WIDTH', value))
        objects_menu.add.selector('Player Pixel Width', [('Classic', 2), ('Filled', 0)], default=0 if player_pixel_width == 2 else 1, onchange=lambda item, value: set_attribute_internal(configurable_options, 'PLAYER_PIXEL_WIDTH', value))
        objects_menu.add.selector('Bullet Pixel Width', [('Classic', 2), ('Filled', 0)], default=0 if bullet_pixel_width == 2 else 1, onchange=lambda item, value: set_attribute_internal(configurable_options, 'BULLET_PIXEL_WIDTH', value))
        objects_menu.add.selector('Star Twinkle Effect', [('On', True), ('Off', False)], default=0 if star_twinkle_effect == True else 1, onchange=lambda item, value: set_attribute_internal(configurable_options, 'STAR_TWINKLE_EFFECT', value))
        objects_menu.add.button('Back', pygame_menu.events.BACK)
        return objects_menu


    def difficulty_menu_internal():
        current_asteroid_kinds = configurable_options.ASTEROID_KINDS
        current_max_asteroids = configurable_options.MAX_ASTEROIDS_ON_SCREEN
        current_max_bullets = configurable_options.PLAYER_MAX_BULLETS_ON_SCREEN
        bullets_collide_with_player = configurable_options.BULLETS_COLLIDE_WITH_PLAYER
        player_lives = configurable_options.PLAYER_LIVES

        player_lives_index = 0
        if player_lives == 2:
            player_lives_index = 1
        elif player_lives == 3:
            player_lives_index = 2

        asteroid_kinds_index = 0
        if current_asteroid_kinds == 4:
            asteroid_kinds_index = 1
        elif current_asteroid_kinds == 5:
            asteroid_kinds_index = 2

        max_asteroids_index = 0
        if current_max_asteroids == 30:
            max_asteroids_index = 1
        elif current_max_asteroids == 45:
            max_asteroids_index = 2

        max_bullets_index = 0
        if current_max_bullets == 10:
            max_bullets_index = 1
        elif current_max_bullets == 15:
            max_bullets_index = 2

        difficulty_menu = pygame_menu.Menu('Difficulty Settings', SCREEN_WIDTH, SCREEN_HEIGHT, theme=asteroids_theme)
        menus.add(difficulty_menu)
        difficulty_menu.add.selector('Player Max Bullets', [('Default', 5), ('Double', 10), ('Triple', 15)], default=max_bullets_index, onchange=lambda item, value: set_attribute_internal(configurable_options, 'PLAYER_MAX_BULLETS_ON_SCREEN', value))
        difficulty_menu.add.selector('Player Lives', [('1', 1), ('2', 2), ('3', 3)], default=player_lives_index, onchange=lambda item, value: set_attribute_internal(configurable_options, 'PLAYER_LIVES', value))
        difficulty_menu.add.selector('Bullets Collide w/Player', [('Off', False), ('On (Friendly Fire)', True)], default=0 if bullets_collide_with_player == False else 1, onchange=lambda item, value: set_attribute_internal(configurable_options, 'BULLETS_COLLIDE_WITH_PLAYER', value))
        difficulty_menu.add.selector('Max Asteroids', [('Default', 15), ('Double', 30), ('Triple', 45)], default=max_asteroids_index, onchange=lambda item, value: set_attribute_internal(configurable_options, 'MAX_ASTEROIDS_ON_SCREEN', value))
        difficulty_menu.add.selector('Asteroid Sizes', [('Default', 3), ('4', 4), ('5', 5)], default=asteroid_kinds_index, onchange=lambda item, value: set_attribute_internal(configurable_options, 'ASTEROID_KINDS', value))
        difficulty_menu.add.button('Back', pygame_menu.events.BACK)
        return difficulty_menu

    menu_background = MenuBackground(configurable_options)
    asteroids_theme.background_color = (0, 0, 0, 0)
        
    menu = pygame_menu.Menu('py-Asteroids', SCREEN_WIDTH, SCREEN_HEIGHT, theme=asteroids_theme)
    menus.add(menu)
    menu.add.button('Play', game_loop_func)
    menu.add.button('Options', options_menu_internal())
    menu.add.button('Quit', pygame_menu.events.EXIT)
    menu.mainloop(screen, bgfun=menu_background.draw)


def pause_menu(screen_obj, game_surface, game_options_obj, theme_obj, game_loop_func):
    menu_background = MenuBackground(game_options_obj)
    theme_obj.background_color = (0, 0, 0, 0)
    
    paused_menu = pygame_menu.Menu('Paused', game_options_obj.SCREEN_WIDTH, game_options_obj.SCREEN_HEIGHT, theme=theme_obj)
    
    action = {'quit_to_main': False}

    def quit_to_main():
        action['quit_to_main'] = True
        paused_menu.disable()

    paused_menu.add.button('Resume', paused_menu.disable)
    paused_menu.add.button('Video Options', video_options())
    paused_menu.add.button('Quit to Main Menu', quit_to_main)
    paused_menu.add.button('Quit to Desktop', lambda: (pygame.quit(), sys.exit()))
    
    paused_menu.mainloop(screen_obj, bgfun=menu_background.draw)
    return action['quit_to_main']

def video_options():
    supported_resolutions = sorted(pygame.display.list_modes())
    resolutions_selector = []
    resolutions_index = 0

    for i in range(len(supported_resolutions)):
        if supported_resolutions[i] == pygame.display.get_surface().get_size():
            resolutions_index = i


    for resolution in supported_resolutions:
        resolutions_selector.append((f"{resolution[0]}x{resolution[1]}", resolution))

    video_menu = pygame_menu.Menu('Video Options', SCREEN_WIDTH, SCREEN_HEIGHT, theme=asteroids_theme)
    menus.add(video_menu)

    def resize_menus():
        for m in menus:
            m.resize(configurable_options.SCREEN_WIDTH, configurable_options.SCREEN_HEIGHT)

    def on_toggle_fullscreen():
        toggle_fullscreen_and_adjust_screen()
        resize_menus()
        
        new_resolutions_index = 0
        current_size = pygame.display.get_surface().get_size()
        for i, item_tuple in enumerate(selector_widget.get_items()):
            value = item_tuple[1]
            if value == current_size:
                new_resolutions_index = i
                break
        selector_widget.set_value(new_resolutions_index)

    video_menu.add.label('Press ENTER to toggle fullscreen', font_size=15, font_color=(255, 255, 255))
    video_menu.add.button('Toggle Fullscreen', on_toggle_fullscreen)
    video_menu.add.label('Press ENTER to apply resolution change', font_size=15, font_color=(255, 255, 255))
    selector_widget = video_menu.add.selector('Resolution', 
        resolutions_selector, 
        default=resolutions_index, 
        onreturn=lambda item, value: (set_resolution(value), resize_menus()))
    video_menu.add.button('Back', pygame_menu.events.BACK)
    return video_menu


def toggle_fullscreen_and_adjust_screen():
    global SCREEN_WIDTH
    global SCREEN_HEIGHT
    global screen

    pygame.display.toggle_fullscreen()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN if pygame.display.get_surface().get_flags() & pygame.FULLSCREEN else 0)

    current_display_info = pygame.display.Info()
    configurable_options.SCREEN_WIDTH = current_display_info.current_w
    configurable_options.SCREEN_HEIGHT = current_display_info.current_h
    SCREEN_WIDTH = current_display_info.current_w
    SCREEN_HEIGHT = current_display_info.current_h

def set_resolution(resolution):
    global SCREEN_WIDTH
    global SCREEN_HEIGHT
    global screen
        
    configurable_options.SCREEN_WIDTH = resolution[0]
    configurable_options.SCREEN_HEIGHT = resolution[1]
    SCREEN_WIDTH = resolution[0]
    SCREEN_HEIGHT = resolution[1]
    screen = pygame.display.set_mode(resolution)