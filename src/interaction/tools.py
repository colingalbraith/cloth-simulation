def select_particle(particles, mouse_pos, drag_radius):
    closest_particle = None
    min_dist = float('inf')

    for row in particles:
        for particle in row:
            dist = (particle.x - mouse_pos[0]) ** 2 + (particle.y - mouse_pos[1]) ** 2
            if dist < min_dist and dist < drag_radius ** 2:
                min_dist = dist
                closest_particle = particle

    return closest_particle

def apply_force_to_particle(particle, force):
    if particle is not None and not particle.fixed:
        particle.apply_force(force)

def cut_cloth(particles, mouse_pos, cut_radius):
    for row in particles:
        for particle in row:
            dist = (particle.x - mouse_pos[0]) ** 2 + (particle.y - mouse_pos[1]) ** 2
            if dist < cut_radius ** 2:
                particle.fixed = True  # Mark the particle as fixed to simulate cutting
                # Optionally, you can also remove springs connected to this particle
                # This would require access to the springs list to remove them accordingly

def distinguish_action(event, particles, mouse_pos, drag_radius, cut_radius):
    if event.button == 1:  # Left mouse button for grabbing
        return select_particle(particles, mouse_pos, drag_radius)
    elif event.button == 3:  # Right mouse button for cutting
        cut_cloth(particles, mouse_pos, cut_radius)
        return None  # No particle to return when cutting

def update_particle_interaction(event, particles, drag_radius, cut_radius):
    mouse_pos = pygame.mouse.get_pos()
    if event.type == pygame.MOUSEBUTTONDOWN:
        return distinguish_action(event, particles, mouse_pos, drag_radius, cut_radius)
    return None
