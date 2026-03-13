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
        if self.target and not self.target.alive():
            self.target = None
            self.target_found = False

        super().update(dt)
        if not self.target_found:
            from asteroid import Asteroid
            closest_asteroid = None
            min_distance = float('inf')
            for asteroid in Asteroid.containers[0]:
                distance = self.position.distance_to(asteroid.position)
                if distance < (self.radius + asteroid.radius) * 3 and distance < min_distance:
                    min_distance = distance
                    closest_asteroid = asteroid
            if closest_asteroid:
                self.target_found = True
                self.target = closest_asteroid
        if self.target is not None:
            direction = self.target.position - self.position
            if direction.length() > 0:
                self.velocity = direction.normalize() * PLAYER_SHOOT_SPEED
                target_rot = math.degrees(math.atan2(self.velocity.y, self.velocity.x)) - 90
                self.rotation += (((target_rot - self.rotation + 180) % 360) - 180) * min(1, dt * 8)

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
    def __init__(self, x, y, width, height, game_options):
        super().__init__(x, y, width, height)
        self.game_options = game_options
        self.time_alive = 0
        self.flicker_timer = 0
        self.flicker = False
        self.contents = random.choices(["homing","laser","1up"], weights=[85,14,1])[0]
    
    def update(self, dt):
        self.time_alive += dt

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
        from missileshape import MissileShape
        from triangleshape import TriangleShape
        player_width = self.game_options.PLAYER_PIXEL_WIDTH
        super().draw(screen)
        rect = pygame.Rect(0, 0, self.width, self.height)
        rect.center = self.position
        if not self.flicker:
            pygame.draw.rect(screen, self.color, rect, LINE_WIDTH)
            if self.contents == "homing":
                icon = MissileShape(self.position.x, self.position.y)
                icon.color = "orange"
                icon.draw(screen)
            elif self.contents == "laser":
                icon1 = TriangleShape((self.vertices[0].x + self.vertices[1].x) / 2, self.position.y - 8, (self.width / 4))
                icon1.points = icon1.get_world_vertices()
                icon1.draw = pygame.draw.polygon(screen, "white", icon1.points, player_width)
                icon2 = pygame.draw.line(screen, "blue", (icon1.points[0].x, icon1.points[0].y), (self.vertices[2] + self.vertices[3]) / 2, 3)
            elif self.contents == "1up":
                shift = self.width*0.08
                gap = max(4, int(self.width*0.08))
                tri_x = rect.left + gap + (self.width/8) + shift 
                icon = TriangleShape(tri_x, self.position.y, (self.width / 4))
                pygame.draw.polygon(screen, "white", icon.get_world_vertices(), player_width) 
                icon_font = pygame.font.Font(None, max(14, int(self.width*0.52)))
                txt_surf = icon_font.render("+1", True, (255,255,255))
                txt_rect = txt_surf.get_rect(midleft=(rect.left + self.width*0.32 + shift, rect.centery))
                screen.blit(txt_surf, txt_rect)
    
        