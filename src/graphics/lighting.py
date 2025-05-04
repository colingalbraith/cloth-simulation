import pygame

class Lighting:
    def __init__(self, ambient_light=0.3, specular_intensity=0.4):
        self.ambient_light = ambient_light
        self.specular_intensity = specular_intensity
        self.light_dir = pygame.Vector2(0.707, -0.707).normalize()

    def calculate_lighting(self, p1, p2, p3):
        edge1 = pygame.Vector2(p2.x - p1.x, p2.y - p1.y)
        edge2 = pygame.Vector2(p3.x - p1.x, p3.y - p1.y)

        normal_z = edge1.cross(edge2)

        if abs(normal_z) < 1e-6:
            return self.ambient_light, 0

        normal = pygame.Vector2(-edge1.y, edge1.x) if normal_z > 0 else pygame.Vector2(edge1.y, -edge1.x)
        normal.normalize_ip()

        diffuse = max(normal.dot(self.light_dir), 0)

        view_dir = pygame.Vector2(0, -1)
        reflect_dir = 2 * normal.dot(self.light_dir) * normal - self.light_dir
        specular = max(reflect_dir.dot(view_dir), 0) ** 32
        specular *= self.specular_intensity

        return self.ambient_light + (1 - self.ambient_light) * diffuse, specular

    def adjust_color(self, base_color, diffuse, specular):
        r = min(255, int(base_color[0] * diffuse) + int(255 * specular))
        g = min(255, int(base_color[1] * diffuse) + int(255 * specular))
        b = min(255, int(base_color[2] * diffuse) + int(255 * specular))
        return (r, g, b)