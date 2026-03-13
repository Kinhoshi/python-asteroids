import pygame

controls = {
    "accelerate": None,
    "acceleratealt": None,
    "rotateleft": None,
    "rotateleftalt": None,
    "rotateright": None,
    "rotaterightalt": None,
    "shoot": None,
    "shootalt": None,
    "pause": None,
    "pausealt": None
}

waiting_for_key = None


def is_control_pressed(control_value):
    if control_value is None:
        return False
    
    # Mouse buttons are negative
    if control_value < 0:
        mouse_buttons = pygame.mouse.get_pressed()
        # -1 -> index 0 (Left), -2 -> index 1 (Middle), etc.
        btn_idx = abs(control_value) - 1
        if 0 <= btn_idx < len(mouse_buttons):
            return mouse_buttons[btn_idx]
        return False
    else:
        keys = pygame.key.get_pressed()
        if 0 <= control_value < len(keys):
            return keys[control_value]
        return False


def get_key_name(value):
    if value is None:
        return "None"
    if value < 0:
        btn = abs(value)
        if btn == 1: return "Mouse Left"
        if btn == 2: return "Mouse Middle"
        if btn == 3: return "Mouse Right"
        return f"Mouse {btn}"
    
    name = pygame.key.name(value)
    return name.upper() if name else str(value)


def load_controls(parser):
    for action in controls:
        if action in parser["Controls"]:
            controls[action] = int(parser["Controls"][action])


def start_rebind(action):
    global waiting_for_key
    waiting_for_key = action


def handle_input_event(event, parser, game_options=None):
    global waiting_for_key

    if waiting_for_key is None:
        return False

    new_value = None
    if event.type == pygame.KEYDOWN:
        if waiting_for_key != "pause" or waiting_for_key != "pausealt":
            if event.key == pygame.K_ESCAPE:
                waiting_for_key = None
                return False
            new_value = event.key
    elif event.type == pygame.MOUSEBUTTONDOWN:
        new_value = -event.button

    if new_value is not None:
        key_map = {
            "accelerate": "Accelerate",
            "acceleratealt": "AccelerateAlt",
            "rotateleft": "RotateLeft",
            "rotateleftalt": "RotateLeftAlt",
            "rotateright": "RotateRight",
            "rotaterightalt": "RotateRightAlt",
            "shoot": "Shoot",
            "shootalt": "ShootAlt",
            "pause": "Pause",
            "pausealt": "PauseAlt"
        }
        attr_map = {
            "accelerate": "CONTROLS_ACCELERATE",
            "acceleratealt": "CONTROLS_ACCELERATE_ALT",
            "rotateleft": "CONTROLS_ROTATE_LEFT",
            "rotateleftalt": "CONTROLS_ROTATE_LEFT_ALT",
            "rotateright": "CONTROLS_ROTATE_RIGHT",
            "rotaterightalt": "CONTROLS_ROTATE_RIGHT_ALT",
            "shoot": "CONTROLS_SHOOT",
            "shootalt": "CONTROLS_SHOOT_ALT",
            "pause": "CONTROLS_PAUSE",
            "pausealt": "CONTROLS_PAUSE_ALT"
        }

        # Unbind any other action using this key
        for action, value in list(controls.items()):
            if value == new_value and action != waiting_for_key:
                # This key is already used by 'action'. Unbind it by setting to 0.
                controls[action] = 0
                
                unbound_config_key = key_map.get(action, action)
                parser["Controls"][unbound_config_key] = '0'

                if game_options:
                    unbound_attr = attr_map.get(action)
                    if unbound_attr:
                        setattr(game_options, unbound_attr, 0)

        # Map internal action to config key
        key_map = {
            "accelerate": "Accelerate",
            "acceleratealt": "AccelerateAlt",
            "rotateleft": "RotateLeft",
            "rotateleftalt": "RotateLeftAlt",
            "rotateright": "RotateRight",
            "rotaterightalt": "RotateRightAlt",
            "shoot": "Shoot",
            "shootalt": "ShootAlt",
            "pause": "Pause",
            "pausealt": "PauseAlt"
        }
        
        config_key = key_map.get(waiting_for_key, waiting_for_key)
        
        parser["Controls"][config_key] = str(new_value)

        with open("config.ini", "w") as configfile:
            parser.write(configfile)

        controls[waiting_for_key] = new_value
        
        if game_options:
            attr = attr_map.get(waiting_for_key)
            if attr:
                setattr(game_options, attr, new_value)

        waiting_for_key = None
        return True
        
    return False