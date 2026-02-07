from constants import *
import pygame
import math
import random

# class for asteroids
class OctagonShape(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius
        self.local_vertices = self.octagon()
        self.rotation = 0
        self.color = "white"
        self.width = getattr(self, "width", LINE_WIDTH) # Pixel width, 0 is filled

    def draw(self, screen):
        color = self.color
        points = self.get_world_vertices()
        pygame.draw.polygon(screen, color, points, self.width)

    def update(self, dt):
        SCREEN_WIDTH = pygame.display.get_surface().get_width()
        SCREEN_HEIGHT = pygame.display.get_surface().get_height()
        if self.position.x > SCREEN_WIDTH:
            self.position.x -= SCREEN_WIDTH
        if self.position.x < 0:
            self.position.x += SCREEN_WIDTH
        if self.position.y > SCREEN_HEIGHT:
            self.position.y -= SCREEN_HEIGHT
        if self.position.y < 0:
            self.position.y += SCREEN_HEIGHT

    def octagon(self):
        points = []

        for i in range(8):
            angle = i * (360 / 8)

            variation = random.uniform(0.8, 1.2)
            radius = self.radius * variation

            x = math.cos(math.radians(angle)) * radius
            y = math.sin(math.radians(angle)) * radius

            points.append(pygame.Vector2(x, y))
        
        center = pygame.Vector2(0, 0)

        for p in points:
            center += p

        center /= len(points)

        return points

    def get_world_vertices(self):
        vertices = []
        for p in self.local_vertices:
            rotated = p.rotate(self.rotation)
            vertices.append(rotated + self.position)
        return vertices

    def get_edges(self):
        vertices = self.get_world_vertices()
        edges = []

        for i in range(len(vertices)):
            start = vertices[i]
            end = vertices[(i + 1) % len(vertices)]
            edges.append((start, end))
        return edges

    def get_perpendicular_normals(self):
        edges = self.get_edges()
        normals = []

        for point_a, point_b in edges:
            edge = point_b - point_a
            normal = pygame.Vector2(-edge.y, edge.x)
            normal = normal.normalize()
            normals.append(normal)
        return normals

    def project_onto_axis(self, axis):
        vertices = self.get_world_vertices()
        projections = [v.dot(axis) for v in vertices]
        return min(projections), max(projections)

    def overlaps(self, minA, maxA, minB, maxB):
        return not (maxA < minB or maxB < minA)

    def overlaps_on_all_axes(self, other):
        for axis in self.get_perpendicular_normals():
            minA, maxA = self.project_onto_axis(axis)
            minB, maxB = other.project_onto_axis(axis)

            if not self.overlaps(minA, maxA, minB, maxB):
                return False

        return True

    def collides_with(self, other):
        if not self.overlaps_on_all_axes(other):
            return False
        if not other.overlaps_on_all_axes(self):
            return False
        return True