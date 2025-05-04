import pygame
import math
import random
import numpy as np
from .particle import Particle
from .spring import Spring

class ClothSystem:
    def __init__(self):
        self.WIDTH = 800
        self.HEIGHT = 800
        self.particles = []
        self.springs = []
        self.gravity = 0.15
        self.damping = 0.99
        self.spring_strength = 0.2
        self.current_tool = "grab"
        
        # Simulation settings
        self.num_iterations = 6
        
        # Cloth appearance
        self.cloth_color_a = (158, 98, 204)
        self.cloth_color_b = (130, 80, 200)
        self.highlight_color = (255, 255, 255)
        
        # Light parameters
        self.ambient_light = 0.3
        self.specular_intensity = 0.4
        self.light_dir = pygame.Vector2(0.707, -0.707).normalize()
        
        # Create initial cloth
        self.create_cloth(30, 25, 12)

    def create_cloth(self, grid_w, grid_h, spacing):
        """Create a cloth grid"""
        self.particles = []
        self.springs = []
        start_x = (self.WIDTH - (grid_w - 1) * spacing) // 2
        start_y = 60

        # Create particles
        for i in range(grid_h):
            row = []
            for j in range(grid_w):
                fixed = i == 0 and j % 3 == 0
                p = Particle(start_x + j * spacing, start_y + i * spacing, fixed)
                row.append(p)
                
                # Create structural springs (horizontal and vertical) with higher strength
                if j > 0: 
                    self.springs.append(Spring(row[j-1], p, strength=0.25, breaking_threshold=8.0))  # Horizontal springs
                if i > 0:
                    self.springs.append(Spring(self.particles[i-1][j], p, strength=0.25, breaking_threshold=8.0))  # Vertical springs
                
                # Create shear springs (diagonals) with higher strength
                if i > 0 and j > 0:
                    self.springs.append(Spring(self.particles[i-1][j-1], p, strength=0.08, breaking_threshold=6.0))
                if i > 0 and j < grid_w-1:
                    self.springs.append(Spring(self.particles[i-1][j+1], p, strength=0.08, breaking_threshold=6.0))
                
                # Add bend resistance springs with higher strength
                if j > 1:  # Horizontal bend springs
                    self.springs.append(Spring(row[j-2], p, strength=0.03, breaking_threshold=5.0))
                if i > 1:  # Vertical bend springs
                    self.springs.append(Spring(self.particles[i-2][j], p, strength=0.03, breaking_threshold=5.0))
            
            self.particles.append(row)

    def create_strip(self):
        """Create a cloth strip"""
        self.create_cloth(45, 8, 10)

    def update(self):
        """Update the cloth physics"""
        # Run multiple iterations for stability
        for _ in range(self.num_iterations):
            # Update springs and remove broken ones
            self.springs = [s for s in self.springs if not s.apply()]
            
            # Update particles
            for row in self.particles:
                for p in row:
                    p.update(self.gravity, self.damping)
            
            # Apply constraints like boundary collisions
            self._apply_constraints()
    
    def _apply_constraints(self):
        """Apply constraints to keep particles within bounds"""
        buffer = 5  # Buffer from edges
        
        for row in self.particles:
            for p in row:
                # Only apply to non-fixed particles
                if not p.fixed:
                    # Constrain to window boundaries with a little bounce
                    if p.x < buffer:
                        p.x = buffer
                        p.px = p.x + (p.x - p.px) * 0.4  # Bounce effect
                    elif p.x > self.WIDTH - buffer:
                        p.x = self.WIDTH - buffer
                        p.px = p.x + (p.x - p.px) * 0.4  # Bounce effect
                        
                    if p.y > self.HEIGHT - buffer:
                        p.y = self.HEIGHT - buffer
                        p.px = p.x + (p.y - p.py) * 0.2  # Reduced bounce for floor

    def draw(self, screen):
        """Draw the cloth to the screen"""
        # Check if we have a grid-like structure
        if len(self.particles) > 1 and all(len(row) > 1 for row in self.particles):
            self._draw_cloth_mesh(screen)
        else:
            self._draw_non_mesh(screen)
    
    def _draw_cloth_mesh(self, screen):
        """Draw cloth as colored triangles with lighting"""
        # Create a set of valid connections for quick lookup
        connections = set()
        for s in self.springs:
            if not s.broken:
                connections.add((s.p1, s.p2))
                connections.add((s.p2, s.p1))
        
        for i in range(len(self.particles) - 1):
            for j in range(len(self.particles[i]) - 1):
                p1 = self.particles[i][j]
                p2 = self.particles[i][j+1]
                p3 = self.particles[i+1][j]
                p4 = self.particles[i+1][j+1]

                # First triangle (if connections exist)
                if (p1, p2) in connections and (p2, p4) in connections and (p1, p4) in connections:
                    diffuse, specular = self._calculate_lighting(p1, p2, p4)
                    color = self._adjust_color(
                        self.cloth_color_a if (i+j)%2 else self.cloth_color_b, 
                        diffuse, specular
                    )
                    pygame.draw.polygon(screen, color, [p1.pos(), p2.pos(), p4.pos()])

                # Second triangle (if connections exist)
                if (p1, p4) in connections and (p4, p3) in connections and (p1, p3) in connections:
                    diffuse, specular = self._calculate_lighting(p1, p4, p3)
                    color = self._adjust_color(
                        self.cloth_color_a if (i+j)%2 else self.cloth_color_b, 
                        diffuse, specular
                    )
                    pygame.draw.polygon(screen, color, [p1.pos(), p4.pos(), p3.pos()])
    
    def _calculate_lighting(self, p1, p2, p3):
        """Calculate lighting for a cloth triangle"""
        edge1 = pygame.Vector2(p2.x - p1.x, p2.y - p1.y)
        edge2 = pygame.Vector2(p3.x - p1.x, p3.y - p1.y)
        
        # For 2D vectors, cross product is a scalar
        normal_z = edge1.cross(edge2)
        
        if abs(normal_z) < 1e-6:
            return self.ambient_light, 0
        
        # Create a normal vector perpendicular to the surface
        normal = pygame.Vector2(-edge1.y, edge1.x) if normal_z > 0 else pygame.Vector2(edge1.y, -edge1.x)
        normal.normalize_ip()
        
        diffuse = max(normal.dot(self.light_dir), 0)
        
        # Specular calculation
        view_dir = pygame.Vector2(0, -1)
        reflect_dir = 2 * normal.dot(self.light_dir) * normal - self.light_dir
        specular = max(reflect_dir.dot(view_dir), 0) ** 32
        specular *= self.specular_intensity
        
        return self.ambient_light + (1 - self.ambient_light) * diffuse, specular
    
    def _adjust_color(self, base_color, diffuse, specular):
        """Adjust color based on lighting"""
        r = min(255, int(base_color[0] * diffuse) + int(255 * specular))
        g = min(255, int(base_color[1] * diffuse) + int(255 * specular))
        b = min(255, int(base_color[2] * diffuse) + int(255 * specular))
        return (r, g, b)
    
    def grab_particle(self, x, y, radius=15):
        """Find and return a particle at the given coordinates"""
        min_dist = float('inf')
        closest_particle = None
        
        for row in self.particles:
            for p in row:
                dist = (p.x - x)**2 + (p.y - y)**2
                if dist < min_dist and dist < radius**2:
                    min_dist = dist
                    closest_particle = p
                    
        return closest_particle
    
    def cut_cloth(self, x, y, radius=20):
        """Cut springs near the given coordinates"""
        springs_to_remove = []
        
        for spring in self.springs:
            # Calculate closest point on spring line to the mouse position
            p1, p2 = spring.p1, spring.p2
            
            # Vector from p1 to p2
            line = (p2.x - p1.x, p2.y - p1.y)
            line_length_squared = line[0]**2 + line[1]**2
            
            if line_length_squared == 0:  # p1 and p2 are the same point
                closest_point = (p1.x, p1.y)
            else:
                # Vector from p1 to mouse
                t = max(0, min(1, ((x - p1.x) * line[0] + (y - p1.y) * line[1]) / line_length_squared))
                closest_point = (p1.x + t * line[0], p1.y + t * line[1])
            
            # Check if the closest point is within the cut radius
            dist = math.hypot(closest_point[0] - x, closest_point[1] - y)
            if dist < radius:
                springs_to_remove.append(spring)
        
        # Remove the springs
        for spring in springs_to_remove:
            if spring in self.springs:
                self.springs.remove(spring)
        
        return len(springs_to_remove) > 0