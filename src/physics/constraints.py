from dataclasses import dataclass
import pygame

@dataclass
class DistanceConstraint:
    p1: 'Particle'
    p2: 'Particle'
    rest_length: float

    def apply(self):
        dx = self.p2.x - self.p1.x
        dy = self.p2.y - self.p1.y
        dist = (dx ** 2 + dy ** 2) ** 0.5

        if dist == 0:
            return

        # Calculate the difference from the rest length
        difference = self.rest_length - dist
        percent = difference / dist * 0.5  # Apply half the correction to each particle

        if not self.p1.fixed:
            self.p1.x += dx * percent
            self.p1.y += dy * percent

        if not self.p2.fixed:
            self.p2.x -= dx * percent
            self.p2.y -= dy * percent

class CollisionConstraint:
    def __init__(self, particle: 'Particle', radius: float):
        self.particle = particle
        self.radius = radius

    def apply(self, boundary_rect: pygame.Rect):
        if self.particle.x < boundary_rect.left:
            self.particle.x = boundary_rect.left
        elif self.particle.x > boundary_rect.right:
            self.particle.x = boundary_rect.right

        if self.particle.y < boundary_rect.top:
            self.particle.y = boundary_rect.top
        elif self.particle.y > boundary_rect.bottom:
            self.particle.y = boundary_rect.bottom

class ClothConstraints:
    def __init__(self, particles: list, boundary_rect: pygame.Rect):
        self.particles = particles
        self.boundary_rect = boundary_rect
        self.distance_constraints = []
        self.collision_constraints = []

    def add_distance_constraint(self, p1: 'Particle', p2: 'Particle'):
        rest_length = ((p2.x - p1.x) ** 2 + (p2.y - p1.y) ** 2) ** 0.5
        self.distance_constraints.append(DistanceConstraint(p1, p2, rest_length))

    def add_collision_constraint(self, particle: 'Particle', radius: float):
        self.collision_constraints.append(CollisionConstraint(particle, radius))

    def apply_constraints(self):
        for constraint in self.distance_constraints:
            constraint.apply()

        for constraint in self.collision_constraints:
            constraint.apply(self.boundary_rect)