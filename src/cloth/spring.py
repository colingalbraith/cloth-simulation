import math


class Spring:
    def __init__(self, p1, p2, strength=0.1, breaking_threshold=5.0):
        self.p1 = p1
        self.p2 = p2

        # Calculate rest length
        dx = p2.x - p1.x
        dy = p2.y - p1.y
        self.rest_length = math.hypot(dx, dy)

        # Spring properties
        self.spring_constant = strength  # Use the provided strength parameter
        self.max_stretch = self.rest_length * breaking_threshold
        self.broken = False

    def apply(self, epsilon=1e-6):
        if self.broken:
            return True

        # Calculate current distance
        dx = self.p2.x - self.p1.x
        dy = self.p2.y - self.p1.y  # FIX: Changed p1.y to self.p1.y
        dist = math.hypot(dx, dy)

        # Check if spring should break
        if dist > self.max_stretch:
            self.broken = True
            return True

        # Avoid division by zero
        if dist < epsilon:
            return False

        # Calculate spring force
        force = (dist - self.rest_length) * self.spring_constant
        fx = dx / dist * force
        fy = dy / dist * force

        # Apply force to both particles
        self.p1.apply_force(fx, fy)
        self.p2.apply_force(-fx, -fy)

        return False

    def draw(self, screen, color):
        pygame.draw.line(screen, color, self.p1.pos(), self.p2.pos(), 2)