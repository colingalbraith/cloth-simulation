import pygame
from cloth.particle import Particle
from cloth.spring import Spring

class MouseHandler:
    def __init__(self, particles, springs, drag_radius=15):
        self.particles = particles
        self.springs = springs
        self.drag_radius = drag_radius
        self.dragging = None

    def handle_mouse_down(self, pos):
        mx, my = pos
        for row in self.particles:
            for p in row:
                if not p.fixed and self._is_within_drag_radius(p, mx, my):
                    self.dragging = p
                    break
            if self.dragging:
                break

    def handle_mouse_up(self):
        self.dragging = None

    def handle_mouse_motion(self, pos):
        if self.dragging:
            mx, my = pos
            self.dragging.x = mx
            self.dragging.y = my

    def handle_mouse_click(self, pos):
        mx, my = pos
        for row in self.particles:
            for p in row:
                if not p.fixed and self._is_within_drag_radius(p, mx, my):
                    self._cut_cloth(p)
                    return

    def _is_within_drag_radius(self, particle, mx, my):
        return (particle.x - mx) ** 2 + (particle.y - my) ** 2 < self.drag_radius ** 2

    def _cut_cloth(self, particle):
        # Logic to cut the cloth at the particle's position
        # This could involve removing springs connected to the particle
        for spring in self.springs[:]:
            if spring.p1 == particle or spring.p2 == particle:
                self.springs.remove(spring)  # Remove the spring to simulate cutting

        # Optionally, you could also mark the particle as fixed or change its properties
        particle.fixed = True  # Example: Fix the particle after cutting

    def update(self):
        # Update logic if needed, e.g., for dragging effects
        pass