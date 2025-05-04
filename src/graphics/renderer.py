import pygame
from src.graphics.lighting import calculate_lighting
from src.cloth.particle import Particle
from src.cloth.spring import Spring

class Renderer:
    def __init__(self, screen):
        self.screen = screen

    def draw_cloth(self, particles, springs):
        connections = set()
        for s in springs:
            connections.add((s.p1, s.p2))
            connections.add((s.p2, s.p1))

        for i in range(len(particles) - 1):
            for j in range(len(particles[i]) - 1):
                p1 = particles[i][j]
                p2 = particles[i][j + 1]
                p3 = particles[i + 1][j]
                p4 = particles[i + 1][j + 1]

                # Draw triangles as solid color with lighting
                if (p1, p2) in connections and (p2, p4) in connections and (p1, p4) in connections:
                    self.draw_triangle(p1, p2, p4)

                if (p1, p4) in connections and (p4, p3) in connections and (p1, p3) in connections:
                    self.draw_triangle(p1, p4, p3)

    def draw_triangle(self, p1, p2, p3):
        # Calculate lighting and color for the triangle
        diffuse, specular = calculate_lighting(p1, p2, p3)
        color = self.adjust_color((255, 255, 255), diffuse, specular)
        pygame.draw.polygon(self.screen, color, [p1.pos(), p2.pos(), p3.pos()])

    def adjust_color(self, base_color, diffuse, specular):
        r = min(255, int(base_color[0] * diffuse) + int(255 * specular))
        g = min(255, int(base_color[1] * diffuse) + int(255 * specular))
        b = min(255, int(base_color[2] * diffuse) + int(255 * specular))
        return (r, g, b)

    def draw_particles(self, particles):
        for row in particles:
            for p in row:
                pygame.draw.circle(self.screen, (255, 255, 255), p.pos(), 4)

    def draw_springs(self, springs):
        for s in springs:
            pygame.draw.line(self.screen, (158, 98, 204), s.p1.pos(), s.p2.pos(), 2)