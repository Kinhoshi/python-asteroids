import pygame
import math
from constants import LINE_WIDTH, BASE_WIDTH, BASE_HEIGHT

class RectangleShape(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.position = pygame.Vector2(x, y)
        self.width = width
        self.height = height
        self.color = "white"
        self.vertices = self.get_world_vertices()

    def draw(self, screen):
        # override
        pass

    def update(self, dt):
        # override
        pass
    
    def get_world_vertices(self):
        return [
            pygame.Vector2(self.position.x - self.width / 2, self.position.y - self.height / 2),
            pygame.Vector2(self.position.x + self.width / 2, self.position.y - self.height / 2),
            pygame.Vector2(self.position.x + self.width / 2, self.position.y + self.height / 2),
            pygame.Vector2(self.position.x - self.width / 2, self.position.y + self.height / 2)
        ]

    def get_edges(self):
        edges = []

        for i in range(len(self.vertices)):
            start = self.vertices[i]
            end = self.vertices[(i + 1) % len(self.vertices)]
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

        