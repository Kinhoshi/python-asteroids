import pygame
import pygame_menu.controls as controls
import pygame_menu.widgets

# 1. Create your custom controller class
class MyCustomController(controls.Controller):
    @staticmethod
    def move_up(event: pygame.event.Event, widget) -> bool:
        # Check if either W or UP arrow key was pressed
        return event.key == pygame.K_s or event.key == pygame.K_DOWN

    @staticmethod
    def move_down(event: pygame.event.Event, widget) -> bool:
        # Check if either S or DOWN arrow key was pressed
        return event.key == pygame.K_w or event.key == pygame.K_UP

    @staticmethod
    def back(event: pygame.event.Event, widget) -> bool:
        # Check if ESCAPE key was pressed
        return event.key == pygame.K_ESCAPE