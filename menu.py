import pygame
import pygame_menu
import sys
import weakref
from config import GameOptions
from menubg import MenuBackground
from pygame_menu_custom_controller import MyCustomController

menus = weakref.WeakSet()

def run_main_menu(screen_obj, game_surface, game_options_obj, theme_obj, game_loop_func):

    screen = screen_obj
    surface = game_surface
    configurable_options = game_options_obj
    asteroids_theme = theme_obj
    SCREEN_WIDTH = configurable_options.SCREEN_WIDTH
    SCREEN_HEIGHT = configurable_options.SCREEN_HEIGHT
    custom_controller = MyCustomController()
    
    # Track the difficulty selector widget to update it when custom options change
    difficulty_selector_tracker = {'widget': None, 'custom_index': None}
    # flag used while building the custom menu to suppress premature marking
    _building_custom_menu = False
    
    def set_attribute_internal(target, attr, value): # function to change GameOptions class items
        config_parser = configurable_options.parser
        match attr:
            case 'ASTEROID_PIXEL_WIDTH':
                config_parser["GameSettings"]["AsteroidPixelWidth"] = str(value)
            case 'BULLET_PIXEL_WIDTH':
                config_parser["GameSettings"]["BulletPixelWidth"] = str(value)
            case 'PLAYER_PIXEL_WIDTH':
                config_parser["GameSettings"]["PlayerPixelWidth"] = str(value)
            case 'STAR_TWINKLE_EFFECT':
                config_parser["GameSettings"]["StarTwinkleEffect"] = str(value)
            case 'MAX_ASTEROIDS_ON_SCREEN':
                config_parser["GameDifficulty"]["MaxAsteroidsOnScreen"] = str(value)
            case 'PLAYER_LIVES':
                config_parser["GameDifficulty"]["StartingLives"] = str(value)
            case 'PLAYER_MAX_BULLETS_ON_SCREEN':
                config_parser["GameDifficulty"]["MaxBulletsOnScreen"] = str(value)
            case 'BULLETS_COLLIDE_WITH_PLAYER':
                config_parser["GameDifficulty"]["BulletsKillPlayer"] = str(value)
            case 'ASTEROID_KINDS':
                config_parser["GameDifficulty"]["MaxTypesOfAsteroids"] = str(value)
            case 'DIFFICULTY':
                config_parser["GameDifficulty"]["Difficulty"] = str(value)
            case _:
                print("Unknown attribute")
                return
        with open("config.ini", "w") as configfile:
            config_parser.write(configfile)
        setattr(target, attr, value)

    def set_difficulty(item, value):
        match value:
            case 'Beginner':
                set_attribute_internal(configurable_options, 'ASTEROID_KINDS', 2)
                set_attribute_internal(configurable_options, 'DIFFICULTY', 'Beginner')
                set_attribute_internal(configurable_options, 'MAX_ASTEROIDS_ON_SCREEN', 5)
                set_attribute_internal(configurable_options, 'PLAYER_LIVES', 5)
                set_attribute_internal(configurable_options, 'PLAYER_MAX_BULLETS_ON_SCREEN', 15)
                set_attribute_internal(configurable_options, 'BULLETS_COLLIDE_WITH_PLAYER', False)

            case 'Easy':
                set_attribute_internal(configurable_options, 'ASTEROID_KINDS', 3)
                set_attribute_internal(configurable_options, 'DIFFICULTY', 'Easy')
                set_attribute_internal(configurable_options, 'MAX_ASTEROIDS_ON_SCREEN', 10)
                set_attribute_internal(configurable_options, 'PLAYER_LIVES', 3)
                set_attribute_internal(configurable_options, 'PLAYER_MAX_BULLETS_ON_SCREEN', 10)
                set_attribute_internal(configurable_options, 'BULLETS_COLLIDE_WITH_PLAYER', False)

            case 'Normal':
                set_attribute_internal(configurable_options, 'ASTEROID_KINDS', 4)
                set_attribute_internal(configurable_options, 'DIFFICULTY', 'Normal')
                set_attribute_internal(configurable_options, 'MAX_ASTEROIDS_ON_SCREEN', 15)
                set_attribute_internal(configurable_options, 'PLAYER_LIVES', 2)
                set_attribute_internal(configurable_options, 'PLAYER_MAX_BULLETS_ON_SCREEN', 5)
                set_attribute_internal(configurable_options, 'BULLETS_COLLIDE_WITH_PLAYER', False)

            case 'Hard':
                set_attribute_internal(configurable_options, 'ASTEROID_KINDS', 5)
                set_attribute_internal(configurable_options, 'DIFFICULTY', 'Hard')
                set_attribute_internal(configurable_options, 'MAX_ASTEROIDS_ON_SCREEN', 30)
                set_attribute_internal(configurable_options, 'PLAYER_LIVES', 1)
                set_attribute_internal(configurable_options, 'PLAYER_MAX_BULLETS_ON_SCREEN', 5)
                set_attribute_internal(configurable_options, 'BULLETS_COLLIDE_WITH_PLAYER', False)

            case 'Cruel':
                set_attribute_internal(configurable_options, 'ASTEROID_KINDS', 5)
                set_attribute_internal(configurable_options, 'DIFFICULTY', 'Cruel')
                set_attribute_internal(configurable_options, 'MAX_ASTEROIDS_ON_SCREEN', 30)
                set_attribute_internal(configurable_options, 'PLAYER_LIVES', 1)
                set_attribute_internal(configurable_options, 'PLAYER_MAX_BULLETS_ON_SCREEN', 5)
                set_attribute_internal(configurable_options, 'BULLETS_COLLIDE_WITH_PLAYER', True)

            case 'Impossible':
                set_attribute_internal(configurable_options, 'ASTEROID_KINDS', 5)
                set_attribute_internal(configurable_options, 'DIFFICULTY', 'Impossible')
                set_attribute_internal(configurable_options, 'MAX_ASTEROIDS_ON_SCREEN', 45)
                set_attribute_internal(configurable_options, 'PLAYER_LIVES', 1)
                set_attribute_internal(configurable_options, 'PLAYER_MAX_BULLETS_ON_SCREEN', 5)
                set_attribute_internal(configurable_options, 'BULLETS_COLLIDE_WITH_PLAYER', True)
            
            case 'Custom':
                # Custom difficulty selected, do nothing (custom options already set)
                pass
                
            case _:
                print("Unknown Difficulty")
                return
    
    def mark_difficulty_as_custom():
        """Check if current settings match a preset; if not, save difficulty as 'Custom' and update display."""
        # Only save as Custom if the current difficulty is a preset (not already Custom)
        # This prevents re-saving Custom on every config reload
        if configurable_options.DIFFICULTY not in ['Custom']:
            current_settings = (
                configurable_options.ASTEROID_KINDS,
                configurable_options.MAX_ASTEROIDS_ON_SCREEN,
                configurable_options.PLAYER_LIVES,
                configurable_options.PLAYER_MAX_BULLETS_ON_SCREEN,
                configurable_options.BULLETS_COLLIDE_WITH_PLAYER
            )
            
            presets = {
                'Beginner': (2, 5, 5, 15, False),
                'Easy': (3, 10, 3, 10, False),
                'Normal': (4, 20, 2, 5, False),
                'Hard': (5, 30, 1, 5, False),
                'Cruel': (5, 30, 1, 5, True),
                'Impossible': (5, 45, 1, 5, True)
            }
            
            # Check if current settings match any preset
            matches_preset = False
            for preset_name, preset_settings in presets.items():
                if current_settings == preset_settings:
                    matches_preset = True
                    break
            
            # If no preset matches, save as 'Custom'
            if not matches_preset:
                set_attribute_internal(configurable_options, 'DIFFICULTY', 'Custom')
        
        # Always update the selector display
        if difficulty_selector_tracker['widget'] is not None and difficulty_selector_tracker['custom_index'] is not None:
            try:
                difficulty_selector_tracker['widget'].set_value(difficulty_selector_tracker['custom_index'])
            except Exception:
                pass

    # Sub-menus
    def options_menu_internal():
        options_menu = pygame_menu.Menu('Options', SCREEN_WIDTH, SCREEN_HEIGHT, theme=asteroids_theme)
        menus.add(options_menu)
        options_menu.add.button('Difficulty Settings', difficulty_menu_internal())
        options_menu.add.button('Object Options', objects_sub_menu_internal())
        options_menu.add.button('Video Options', video_options(screen_obj, game_options_obj, theme_obj))
        options_menu.add.button('Control Settings', control_options_menu(screen_obj, game_options_obj, theme_obj))
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
        difficulty_index = 0
        difficulty = configurable_options.DIFFICULTY
        difficulties = [('Beginner', 'Beginner'),('Easy', 'Easy'), ('Normal', 'Normal'), ('Hard', 'Hard'), ('Cruel', 'Cruel'), ('Impossible', 'Impossible'), ('Custom', 'Custom')]
        for i in range(len(difficulties)):
            if difficulties[i][0] == difficulty:
                difficulty_index = i
                break
        difficulty_menu = pygame_menu.Menu('Difficulty Settings', SCREEN_WIDTH, SCREEN_HEIGHT, theme=asteroids_theme)
        menus.add(difficulty_menu)
        selector_widget = difficulty_menu.add.selector('Difficulty', difficulties, default=difficulty_index, onchange=set_difficulty)
        difficulty_selector_tracker['widget'] = selector_widget
        difficulty_selector_tracker['custom_index'] = len(difficulties) - 1
        # custom menu built at creation; initialization flag prevents early marking
        difficulty_menu.add.button('Custom', custom_difficulty_menu_internal())
        difficulty_menu.add.button('Back', pygame_menu.events.BACK)
        return difficulty_menu

    def custom_difficulty_menu_internal():
        # flag to prevent mark during initial construction
        nonlocal _building_custom_menu
        _building_custom_menu = True
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
        elif player_lives == 5:
            player_lives_index = 3

        asteroid_kinds_index = 0
        asteroid_kind_selections = [('2', 2), ('3', 3), ('4', 4), ('5', 5)]
        for i in range(len(asteroid_kind_selections)):
            if asteroid_kind_selections[i][0] == str(current_asteroid_kinds):
                asteroid_kinds_index = i
                break

        max_asteroids_index = 0
        max_asteroids_selections = [('5', 5), ('10', 10), ('15', 15), ('20', 20), ('30', 30), ('45', 45)]
        for i in range(len(max_asteroids_selections)):
            if max_asteroids_selections[i][0] == str(current_max_asteroids):
                max_asteroids_index = i
                break

        max_bullets_index = 0
        if current_max_bullets == 10:
            max_bullets_index = 1
        elif current_max_bullets == 15:
            max_bullets_index = 2

        custom_difficulty_menu = pygame_menu.Menu('Custom Difficulty Settings', SCREEN_WIDTH, SCREEN_HEIGHT, theme=asteroids_theme)
        menus.add(custom_difficulty_menu)
        custom_difficulty_menu.add.label('Max bullets on screen at one time; default is 5', font_size=15, font_color='white')
        # helper to update attribute only when it actually changes
        def custom_option_changed(attr, value):
            if getattr(configurable_options, attr) != value:
                set_attribute_internal(configurable_options, attr, value)
                if not _building_custom_menu:
                    mark_difficulty_as_custom()
        
        custom_difficulty_menu.add.selector('Player Max Bullets', [('Default', 5), ('Double', 10), ('Triple', 15)], default=max_bullets_index, onchange=lambda item, value: custom_option_changed('PLAYER_MAX_BULLETS_ON_SCREEN', value))
        custom_difficulty_menu.add.selector('Player Lives', [('1', 1), ('2', 2), ('3', 3), ('5', 5)], default=player_lives_index, onchange=lambda item, value: custom_option_changed('PLAYER_LIVES', value))
        custom_difficulty_menu.add.label('Allows your own bullets to collide with you; essentially friendly fire.', font_size=15, font_color='white')
        custom_difficulty_menu.add.selector('Bullets Collide w/Player', [('Off', False), ('On', True)], default=0 if bullets_collide_with_player == False else 1, onchange=lambda item, value: custom_option_changed('BULLETS_COLLIDE_WITH_PLAYER', value))
        custom_difficulty_menu.add.label('Prevents asteroids from spawning endlessly; default is 15', font_size=15, font_color='white')
        custom_difficulty_menu.add.selector('Max Asteroids', max_asteroids_selections, default=max_asteroids_index, onchange=lambda item, value: custom_option_changed('MAX_ASTEROIDS_ON_SCREEN', value))
        custom_difficulty_menu.add.label('Allows bigger asteroids to spawn; default is 3 different sizes', font_size=15, font_color='white')
        custom_difficulty_menu.add.selector('Asteroid Sizes', asteroid_kind_selections, default=asteroid_kinds_index, onchange=lambda item, value: custom_option_changed('ASTEROID_KINDS', value))
        custom_difficulty_menu.add.button('Back', pygame_menu.events.BACK)
        _building_custom_menu = False
        return custom_difficulty_menu



    menu_background = MenuBackground(configurable_options)
    asteroids_theme.background_color = (0, 0, 0, 0)
        
    menu = pygame_menu.Menu('py-Asteroids', SCREEN_WIDTH, SCREEN_HEIGHT, theme=asteroids_theme)
    menu.set_controller(custom_controller)
    menus.add(menu)
    menu.add.button('Play', game_loop_func)
    menu.add.button('Options', options_menu_internal())
    menu.add.button('Quit', pygame_menu.events.EXIT)
    while menu.is_enabled():
        all_events = pygame.event.get()
        for event in all_events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        menu.mainloop(screen, bgfun=lambda: menu_background.draw(screen), disable_event=True, events=all_events)


# Pause menu
def pause_menu(screen_obj, game_surface, game_options_obj, theme_obj, game_loop_func):
    custom_controller = MyCustomController()
    menu_background = MenuBackground(game_options_obj)
    theme_obj.background_color = (0, 0, 0, 0)
    
    paused_menu = pygame_menu.Menu('Paused', game_options_obj.SCREEN_WIDTH, game_options_obj.SCREEN_HEIGHT, theme=theme_obj)
    paused_menu.set_controller(custom_controller)
    menus.add(paused_menu)
    
    action = {'quit_to_main': False}

    def quit_to_main(): # function to quit game and return to main menu
        action['quit_to_main'] = True
        paused_menu.disable()

    paused_menu.add.button('Resume', paused_menu.disable)
    paused_menu.add.button('Video Options', video_options(screen_obj, game_options_obj, theme_obj))
    paused_menu.add.button('Control Settings', control_options_menu(screen_obj, game_options_obj, theme_obj))
    paused_menu.add.button('Quit to Main Menu', quit_to_main)
    paused_menu.add.button('Quit to Desktop', lambda: (pygame.quit(), sys.exit()))
    while paused_menu.is_enabled():
        all_events = pygame.event.get()
        for event in all_events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        paused_menu.mainloop(screen_obj, bgfun=lambda:menu_background.draw(screen_obj))
    return action['quit_to_main']

# Video menu, accessible via main menu and pause menu
def video_options(screen_obj, game_options_obj, theme_obj):
    supported_resolutions = sorted(pygame.display.list_modes())
    resolutions_selector = []
    resolutions_index = 0
    configurable_options = game_options_obj
    SCREEN_WIDTH = configurable_options.SCREEN_WIDTH
    SCREEN_HEIGHT = configurable_options.SCREEN_HEIGHT
    asteroids_theme = theme_obj

    for i in range(len(supported_resolutions)):
        if supported_resolutions[i] == pygame.display.get_surface().get_size():
            resolutions_index = i


    for resolution in supported_resolutions:
        resolutions_selector.append((f"{resolution[0]}x{resolution[1]}", resolution))

    video_menu = pygame_menu.Menu('Video Options', SCREEN_WIDTH, SCREEN_HEIGHT, theme=asteroids_theme)
    menus.add(video_menu)

    def resize_menus(): # resize the menu based on current width, height
        for m in menus:
            m.resize(configurable_options.SCREEN_WIDTH, configurable_options.SCREEN_HEIGHT)

    def on_toggle_fullscreen(): # function to call fullscreen function and resize menus
        toggle_fullscreen_and_adjust_screen(screen_obj, game_options_obj)
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
        onreturn=lambda item, value: (set_resolution(screen_obj, game_options_obj, value), resize_menus()))
    video_menu.add.button('Back', pygame_menu.events.BACK)
    return video_menu


def toggle_fullscreen_and_adjust_screen(screen_obj, game_options_obj): # function to toggle fullscreen and set SCREEN WIDTH & HEIGHT to the new resolution
    configurable_options = game_options_obj
    screen = screen_obj

    pygame.display.toggle_fullscreen()

    is_fullscreen = pygame.display.get_surface().get_flags() & pygame.FULLSCREEN
    if is_fullscreen:
        info = pygame.display.Info()
        resolution = (info.current_w, info.current_h)
        screen = pygame.display.set_mode(resolution, pygame.FULLSCREEN)
    else:
        resolution = (800, 600)
        screen = pygame.display.set_mode(resolution)

    configurable_options.SCREEN_WIDTH = resolution[0]
    configurable_options.SCREEN_HEIGHT = resolution[1]
    SCREEN_WIDTH = resolution[0]
    SCREEN_HEIGHT = resolution[1]

    for m in menus:
        m._surface = screen

def set_resolution(screen_obj, game_options_obj, resolution): # function to set SCREEN WIDTH & HEIGHT to the resolution passed in
    configurable_options = game_options_obj
    screen = screen_obj 
    configurable_options.SCREEN_WIDTH = resolution[0]
    configurable_options.SCREEN_HEIGHT = resolution[1]
    SCREEN_WIDTH = resolution[0]
    SCREEN_HEIGHT = resolution[1]
    configurable_options.parser["VideoSettings"]["Width"] = str(resolution[0])
    configurable_options.parser["VideoSettings"]["Height"] = str(resolution[1])
    with open("config.ini", "w") as configfile:
        configurable_options.parser.write(configfile)
    
    if pygame.display.get_surface().get_flags() & pygame.FULLSCREEN:
        for m in menus:
            m._surface = pygame.display.set_mode(resolution)
        pygame.display.set_mode(resolution)
        pygame.display.set_mode(resolution, pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode(resolution)

    for m in menus:
        m._surface = screen

def control_options_menu(screen_obj, game_options_obj, theme_obj):
    configurable_options = game_options_obj
    SCREEN_WIDTH = configurable_options.SCREEN_WIDTH
    SCREEN_HEIGHT = configurable_options.SCREEN_HEIGHT
    asteroids_theme = theme_obj

    controls_menu = pygame_menu.Menu('Control Settings', SCREEN_WIDTH, SCREEN_HEIGHT, theme=asteroids_theme)
    menus.add(controls_menu)
    controls_menu.add.button('Back', pygame_menu.events.BACK)
    return controls_menu