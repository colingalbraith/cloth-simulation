import pygame
import math
import random  # Import random for initial displacement

class Particle:
    def __init__(self, x, y, fixed=False):
        self.x = x
        self.y = y
        self.px = x  # previous x position
        self.py = y  # previous y position
        self.fx = 0  # force accumulator x
        self.fy = 0  # force accumulator y
        self.fixed = fixed
        self.mass = 1.0
        
        # Add a small initial displacement to avoid grid-like appearance
        if not fixed:
            self.px += (random.random() * 2 - 1) * 0.1
            self.py += (random.random() * 2 - 1) * 0.1

    def apply_force(self, fx, fy):
        if not self.fixed:
            self.fx += fx
            self.fy += fy
    
    def update(self, gravity=0.2, damping=0.98):
        if self.fixed:
            return
            
        # Apply gravity
        self.fy += gravity * self.mass
        
        # Verlet integration
        temp_x = self.x
        temp_y = self.y
        
        # Calculate new position with velocity clamping for stability
        vel_x = (self.x - self.px) * damping + self.fx
        vel_y = (self.y - self.py) * damping + self.fy
        
        # Limit velocity for stability (prevent extreme movements)
        max_vel = 10.0
        vel_magnitude = math.hypot(vel_x, vel_y)
        if vel_magnitude > max_vel:
            vel_x = vel_x / vel_magnitude * max_vel
            vel_y = vel_y / vel_magnitude * max_vel
            
        self.x += vel_x
        self.y += vel_y
        
        # Update previous position
        self.px = temp_x
        self.py = temp_y
        
        # Reset forces
        self.fx = 0
        self.fy = 0
    
    def pos(self):
        return (int(self.x), int(self.y))