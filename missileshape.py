import pygame
from constants import BASE_WIDTH, BASE_HEIGHT, PARTICLE_RADIUS
from thrust_particles import Particle



class MissileShape(pygame.sprite.Sprite):
    def __init__(self, x, y):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.rotation = 0
        self.color = "white"
        self.local_vertices = [
            pygame.Vector2(0, 6),     # Tip
            pygame.Vector2(2, 2),     # Shoulder Right
            pygame.Vector2(2, -4),    # Body Right
            pygame.Vector2(4, -6),    # Fin Right
            pygame.Vector2(0, -4),    # Base Center
            pygame.Vector2(-4, -6),   # Fin Left
            pygame.Vector2(-2, -4),   # Body Left
            pygame.Vector2(-2, 2)     # Shoulder Left
        ]
        self.radius = max(v.length() for v in self.local_vertices)


    def draw(self, screen):
        points = self.get_world_vertices()
        pygame.draw.polygon(screen, self.color, points, 2)

    def update(self, dt):
        self.position += self.velocity * dt

        SCREEN_WIDTH = BASE_WIDTH
        SCREEN_HEIGHT = BASE_HEIGHT
        if self.position.x > SCREEN_WIDTH:
            self.position.x -= SCREEN_WIDTH
        if self.position.x < 0:
            self.position.x += SCREEN_WIDTH
        if self.position.y > SCREEN_HEIGHT:
            self.position.y -= SCREEN_HEIGHT
        if self.position.y < 0:
            self.position.y += SCREEN_HEIGHT

        base_pos_local = self.local_vertices[4]
        base_pos_world = self.position + base_pos_local.rotate(self.rotation)
        Particle(base_pos_world.x, base_pos_world.y, (PARTICLE_RADIUS / 2))

    def get_world_vertices(self):
        vertices = []
        for p in self.local_vertices:
            rotated = p.rotate(self.rotation)
            vertices.append(self.position + rotated)
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
            if normal.length() == 0:
                continue
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
    