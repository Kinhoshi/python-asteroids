from shot import Shot
from constants import PLAYER_SHOOT_SPEED, LINE_WIDTH
from rectangleshape import RectangleShape
import pygame
import math
import random

class HomingMissile(Shot):
    def __init__(self, x, y, game_options):
        super().__init__(x, y, game_options)
        self.target = None
        self.target_found = False
        self.color = "orange"


    def update(self, dt):
        from asteroid import Asteroid
        if self.target and (not self.target.alive() or self.target not in Asteroid.containers[0]):
            self.target = None
            self.target_found = False

        super().update(dt)
        if not self.target_found:
            for asteroid in Asteroid.containers[0]:
                if self.position.distance_to(asteroid.position) < (self.radius + asteroid.radius) * 3:
                    self.target_found = True
                    self.target = asteroid
                    break
        if self.target is not None:
            direction = self.target.position - self.position
            if direction.length() > 0:
                self.velocity = direction.normalize() * PLAYER_SHOOT_SPEED

class Laser(Shot):
    def __init__(self, x, y, rotation, game_options):
        super().__init__(x, y, game_options)
        self.rotation = rotation
        self.width = 5
        self.color = "blue"

    def draw(self, screen):
        # Calculate direction from rotation.
        # Player's 0 rotation is down (positive Y), which is +90 degrees in standard trig.
        angle_rad = math.radians(self.rotation + 90)
        direction = pygame.Vector2(math.cos(angle_rad), math.sin(angle_rad))
        
        # Find intersection with screen edge
        # Scale direction to reach beyond screen bounds
        max_distance = math.sqrt(screen.get_width()**2 + screen.get_height()**2)
        end_point = self.position + direction * max_distance
        
        pygame.draw.line(screen, self.color, self.position, end_point, self.width)

    def update(self, dt):
        # Override Shot's update. Laser position is controlled by Player.
        pass

    def collides_with(self, other):
        from asteroid import Asteroid
        if isinstance(other, Asteroid):
            # Calculate direction from rotation
            angle_rad = math.radians(self.rotation + 90)
            direction = pygame.Vector2(math.cos(angle_rad), math.sin(angle_rad))
            
            # Project asteroid position onto the laser line
            v = other.position - self.position
            t = v.dot(direction)
            t = max(0, t) # Laser only goes forward
            
            closest_point = self.position + direction * t
            return closest_point.distance_to(other.position) < (self.width / 2 + other.radius)
        return False

class PowerUp_Box(RectangleShape):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.time_alive = 0
        self.flicker_timer = 0
        self.flicker = False
    
    def update(self, dt):
        self.time_alive += dt
        print(self.time_alive)
        

        if self.time_alive > 20:
            self.kill()
        elif self.time_alive >= 10:
            self.flicker_timer += dt
            if self.time_alive >= 15:
                if self.flicker_timer > 0.2:
                    self.flicker = not self.flicker
                    self.flicker_timer = 0
            if self.time_alive >= 18:
                if self.flicker_timer >= 0.05:
                    self.flicker = not self.flicker
                    self.flicker_timer = 0
            if self.flicker_timer > 0.5:
                self.flicker = not self.flicker
                self.flicker_timer = 0

    def draw(self, screen):
        super().draw(screen)
        rect = pygame.Rect(0, 0, self.width, self.height)
        rect.center = self.position
        if not self.flicker:
            pygame.draw.rect(screen, self.color, rect, LINE_WIDTH)

    
        