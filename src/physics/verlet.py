import pygame
import math

class Verlet:
    @staticmethod
    def update_particle(particle, delta_time):
        if not particle.fixed:
            # Calculate the new position based on the Verlet integration
            temp_x = particle.x
            temp_y = particle.y
            
            # Update position based on previous position and current forces
            particle.x += (particle.x - particle.px) + particle.fx * delta_time ** 2
            particle.y += (particle.y - particle.py) + particle.fy * delta_time ** 2
            
            # Store the previous position
            particle.px = temp_x
            particle.py = temp_y
            
            # Reset forces
            particle.fx = 0
            particle.fy = 0

    @staticmethod
    def apply_constraints(particles, constraints):
        for constraint in constraints:
            constraint.apply(particles)

    @staticmethod
    def integrate(particles, delta_time):
        for particle in particles:
            Verlet.update_particle(particle, delta_time)

        # Apply constraints after updating positions
        Verlet.apply_constraints(particles, constraints)