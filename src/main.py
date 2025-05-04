import pygame
from cloth.cloth_system import ClothSystem
from ui.interface import Interface

def main():
    pygame.init()

    # Screen dimensions
    WIDTH, HEIGHT = 800, 800
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Enhanced Cloth Simulation")

    # Initialize cloth simulation
    cloth_system = ClothSystem()
    interface = Interface()

    # Main loop
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Handle mouse interactions
            interface.handle_event(event, cloth_system)

        # Update the cloth simulation
        cloth_system.update()

        # Render everything
        screen.fill((18, 22, 40))  # Background color
        cloth_system.draw(screen)
        interface.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()