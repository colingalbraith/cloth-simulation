import pygame
from .button import Button

class Interface:
    def __init__(self):
        self.WIDTH = 800
        self.HEIGHT = 800
        self.buttons = self._create_buttons()
        self.dragging_particle = None
        self.current_tool = "grab"  # "grab" or "cut"
        self.tool_buttons = self._create_tool_buttons()
        self.option_buttons = self._create_option_buttons()
        self.highlight_color = (255, 255, 255)
        self.button_color = (40, 45, 60)
        self.tool_button_size = (50, 30)
        self.tool_area = pygame.Rect(290, self.HEIGHT-50, 110, 30)
        self.font = pygame.font.Font(None, 24)
    
    def _create_buttons(self):
        """Create cloth type buttons"""
        return [
            Button(20, self.HEIGHT-50, 80, 30, "Cloth", lambda cs: cs.create_cloth(30, 25, 12)),
            Button(110, self.HEIGHT-50, 80, 30, "Strip", lambda cs: cs.create_strip()),
        ]
    
    def _create_tool_buttons(self):
        """Create tool selection buttons"""
        return [
            Button(290, self.HEIGHT-50, 50, 30, "Grab", lambda: self._set_tool("grab")),
            Button(350, self.HEIGHT-50, 50, 30, "Cut", lambda: self._set_tool("cut")),
        ]
    
    def _create_option_buttons(self):
        """Create option buttons"""
        return []
    
    def _set_tool(self, tool):
        self.current_tool = tool
    
    def handle_event(self, event, cloth_system):
        """Handle user input events"""
        # Handle cloth selection buttons
        for button in self.buttons:
            if button.is_clicked(event):
                button.action(cloth_system)
                self.dragging_particle = None
                return
        
        # Handle tool selection buttons
        for button in self.tool_buttons:
            if button.is_clicked(event):
                button.action()
                return
        
        # Handle option buttons
        for button in self.option_buttons:
            if button.is_clicked(event):
                button.action(cloth_system)
                return
                
        # Handle mouse interaction with cloth
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            
            # Skip if clicked on UI elements
            if any(b.rect.collidepoint(event.pos) for b in self.buttons + self.tool_buttons + self.option_buttons):
                return
                
            # Handle based on current tool
            if self.current_tool == "grab":
                self.dragging_particle = cloth_system.grab_particle(mx, my)
            elif self.current_tool == "cut":
                cloth_system.cut_cloth(mx, my)
                
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging_particle = None
        
        # Update the grabbed particle position
        if self.dragging_particle and not self.dragging_particle.fixed:
            mx, my = pygame.mouse.get_pos()
            self.dragging_particle.x = mx
            self.dragging_particle.y = my
    
    def draw(self, screen):
        """Draw the interface"""
        # Draw cloth type buttons
        for button in self.buttons:
            button.draw(screen)
            
        # Draw tool buttons
        for button in self.tool_buttons:
            button.draw(screen, button.text.lower() == self.current_tool)
        
        # Draw option buttons
        for button in self.option_buttons:
            button.draw(screen)
        
        # Draw cursor based on tool
        mx, my = pygame.mouse.get_pos()
        if self.current_tool == "grab":
            pygame.draw.circle(screen, (200, 200, 255, 128), (mx, my), 15, 1)
        elif self.current_tool == "cut":
            pygame.draw.circle(screen, (255, 100, 100, 128), (mx, my), 20, 1)
            pygame.draw.line(screen, (255, 100, 100), (mx-15, my), (mx+15, my), 1)
            pygame.draw.line(screen, (255, 100, 100), (mx, my-15), (mx, my+15), 1)