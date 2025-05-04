import pygame

class Button:
    def __init__(self, x, y, width, height, text, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.normal_color = (40, 45, 60)
        self.hover_color = (60, 65, 80)
        self.active_color = (70, 90, 120)
        self.text = text
        self.font = pygame.font.Font(None, 24)
        self.action = action
        self.hover = False

    def draw(self, screen, active=False):
        # Choose color based on state
        color = self.active_color if active else (self.hover_color if self.hover else self.normal_color)
        
        # Draw button
        pygame.draw.rect(screen, color, self.rect, border_radius=4)
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        screen.blit(text_surface, (
            self.rect.x + (self.rect.width - text_surface.get_width()) // 2,
            self.rect.y + (self.rect.height - text_surface.get_height()) // 2)
        )
        
        # Update hover state
        mx, my = pygame.mouse.get_pos()
        self.hover = self.rect.collidepoint((mx, my))

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            return self.rect.collidepoint(event.pos)
        return False