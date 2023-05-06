import pygame
import random
import math
from pygame.locals import *
import resources
import resources.constants

pygame.init()
pygame.display.set_caption("Gravity Simulation")

# Generate random particles
for i in range(resources.constants.NUM_PARTICLES):
    if i == 0:
        x = resources.constants.WIDTH // 2
        y = resources.constants.HEIGHT// 2
        mass = 60
        resources.constants.PARTICLES.append(resources.Particle(x, y, mass, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), random.randint(30, 30), pygame.Vector2(0, 0)))
    else:
        x = random.randint(0, resources.constants.WIDTH)
        y = random.randint(0, resources.constants.HEIGHT)
        mass = random.uniform(1, 10)
        mass = 5
        resources.constants.PARTICLES.append(resources.Particle(x, y, mass, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), random.randint(0, 5), pygame.Vector2(0, 0)))

# Initialize button states
increase_button_stateR = False
decrease_button_stateR = False

increase_button_stateM = False
decrease_button_stateM = False

increase_button_stateVx = False
decrease_button_stateVx = False

increase_button_stateVy = False
decrease_button_stateVy = False

add_button_statement = False
add_button_statement_put = False

reset_button_statement = False
reset_scale_button_statement = False

move_particles = False
pause = False

selected_particle = None

def decrease_radius():
    if resources.constants.ADDED_RADIUS-1 != 0:
        resources.constants.ADDED_RADIUS -= 1
    return resources.constants.ADDED_RADIUS
def increase_radius():
    resources.constants.ADDED_RADIUS += 1
    return resources.constants.ADDED_RADIUS
def decrease_mass():
    if resources.constants.ADDED_MASS-1 != 0:
        resources.constants.ADDED_MASS -= 1
    return resources.constants.ADDED_MASS
def increase_mass():
    resources.constants.ADDED_MASS += 1
    return resources.constants.ADDED_MASS
def decrease_velocity_x():
    if not add_button_statement_put:
        resources.constants.ADDED_VELOCITY.x -= 0.05
    return resources.constants.ADDED_VELOCITY.x 
def increase_velocity_x():
    if not add_button_statement_put:
        resources.constants.ADDED_VELOCITY.x += 0.05
    return resources.constants.ADDED_VELOCITY.x 
def decrease_velocity_y():
    if not add_button_statement_put:
        resources.constants.ADDED_VELOCITY.y -= 0.05
    return resources.constants.ADDED_VELOCITY.y
def increase_velocity_y():
    if not add_button_statement_put:
        resources.constants.ADDED_VELOCITY.y += 0.05
    return resources.constants.ADDED_VELOCITY.y
def reset_particles():
    global reset_button_statement
    resources.constants.NUM_PARTICLES = 0
    resources.constants.PARTICLES = []
    reset_button_statement = False
    return resources.constants.NUM_PARTICLES, resources.constants.PARTICLES
def reset_scale():
    global reset_scale_button_statement
    resources.constants.SCALE = 1
    reset_scale_button_statement = False
    return resources.constants.SCALE 

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # Left click
                # Check if the mouse click is inside the buttons
                if button_increse_r.button_rect.collidepoint(event.pos):
                    increase_button_stateR = True
                elif button_decrese_r.button_rect.collidepoint(event.pos):
                    decrease_button_stateR = True
                elif button_increse_m.button_rect.collidepoint(event.pos):
                    increase_button_stateM = True
                elif button_decrese_m.button_rect.collidepoint(event.pos):
                    decrease_button_stateM = True
                elif button_increse_vx.button_rect.collidepoint(event.pos):
                    increase_button_stateVx = True
                elif button_decrese_vx.button_rect.collidepoint(event.pos):
                    decrease_button_stateVx = True
                elif button_increse_vy.button_rect.collidepoint(event.pos):
                    increase_button_stateVy = True
                elif button_decrese_vy.button_rect.collidepoint(event.pos):
                    decrease_button_stateVy = True
                elif add_button.button_rect.collidepoint(event.pos):
                    add_button_statement = True
                elif add_button_statement:
                    add_button_statement_put = True
                elif reset_button.button_rect.collidepoint(event.pos):
                    reset_button_statement = True
                elif reset_scale_button.button_rect.collidepoint(event.pos):
                    reset_scale_button_statement = True
                for particle in resources.constants.PARTICLES:
                    scaled_x = int(resources.constants.MOUSE_X + (particle.position.x - resources.constants.MOUSE_X) * resources.constants.SCALE)
                    scaled_y = int(resources.constants.MOUSE_Y + (particle.position.y - resources.constants.MOUSE_Y) * resources.constants.SCALE)
                    distance = math.sqrt((event.pos[0] - scaled_x)**2 + (event.pos[1] - scaled_y)**2)
                    if distance <= particle.radius * resources.constants.SCALE:
                        particle.selected = not particle.selected

            if event.button == 3: # Right click
                if add_button_statement:
                    add_button_statement = False
            elif event.button == 4:  # Scroll Up
                resources.constants.SCALE += 0.1
                resources.constants.MOUSE_X, resources.constants.MOUSE_Y = pygame.mouse.get_pos()
                
            elif event.button == 5:  # Scroll Down
                if resources.constants.SCALE - 0.1 > 0:
                    resources.constants.SCALE -= 0.1
                    resources.constants.MOUSE_X, resources.constants.MOUSE_Y = pygame.mouse.get_pos()
                
        elif event.type == pygame.MOUSEBUTTONUP:
            initial_mouse_pos = None
            if event.button == 1:
                # Reset button states
                increase_button_stateR = False
                decrease_button_stateR = False
                increase_button_stateM = False
                decrease_button_stateM = False
                increase_button_stateVx = False
                decrease_button_stateVx = False
                increase_button_stateVy = False
                decrease_button_stateVy = False
                
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                move_particles = True
                move_direction = pygame.Vector2(5, 0)
            elif event.key == pygame.K_RIGHT:
                move_particles = True
                move_direction = pygame.Vector2(-5, 0)
            elif event.key == pygame.K_UP:
                move_particles = True
                move_direction = pygame.Vector2(0, 5)
            elif event.key == pygame.K_DOWN:
                move_particles = True
                move_direction = pygame.Vector2(0, -5)
            elif event.key == pygame.K_SPACE:
                pause = not pause
        elif event.type == pygame.KEYUP:
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]:
                move_particles = False

    
    # Draw the background image on the screen
    resources.constants.SCREEN.fill((20,20,40))
    #screen.blit(background_image, (0, 0))

    if increase_button_stateR:
        increase_radius()
    elif decrease_button_stateR:
        decrease_radius()
    elif increase_button_stateM:
        increase_mass()
    elif decrease_button_stateM:
        decrease_mass()
    elif increase_button_stateVx:
        increase_velocity_x()
    elif decrease_button_stateVx:
        decrease_velocity_x()
    elif increase_button_stateVy:
        increase_velocity_y()
    elif decrease_button_stateVy:
        decrease_velocity_y()
    elif reset_button_statement:
        reset_particles()
    elif reset_scale_button_statement:
        reset_scale()

    if add_button_statement:
        actual_mouse_x, actuale_mouse_y = pygame.mouse.get_pos()
        scaled_mouse_x = int(resources.constants.MOUSE_X + (actual_mouse_x - resources.constants.MOUSE_X) * resources.constants.SCALE)
        scaled_mouse_y = int(resources.constants.MOUSE_Y + (actuale_mouse_y - resources.constants.MOUSE_Y) * resources.constants.SCALE)
        circle_center = (scaled_mouse_x, scaled_mouse_y)
        circle_radius = int(resources.constants.ADDED_RADIUS * resources.constants.SCALE)
        pygame.draw.circle(
            resources.constants.SCREEN, 
            resources.constants.ADDED_COLOR , 
            circle_center, 
            circle_radius
            )

    if add_button_statement_put:
        particle_velocity = resources.constants.ADDED_VELOCITY.copy()
        resources.constants.PARTICLES.append(
            resources.Particle(
                actual_mouse_x,
                actuale_mouse_y,
                resources.constants.ADDED_MASS,
                resources.constants.ADDED_COLOR ,
                resources.constants.ADDED_RADIUS,
                particle_velocity
            )
        )
        add_button_statement_put = False
        resources.constants.ADDED_COLOR  = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        resources.constants.NUM_PARTICLES += 1

    # Sort in case bigger particles do not cover smaller ones 
    resources.constants.PARTICLES = sorted(resources.constants.PARTICLES, key=lambda x: x.radius, reverse=True)
    for particle in resources.constants.PARTICLES:
        if move_particles:
            particle.position += move_direction * resources.constants.SCALE
        elif pause:
            pass
        else:
            particle.update()
        
            for other_particle in resources.constants.PARTICLES:
                if particle != other_particle:
                    particle.apply_gravitational_force(other_particle, resources.constants.G)
        particle.draw_scaled(resources.constants.MOUSE_X, resources.constants.MOUSE_Y)

    # Buttons
    button_increse_r = resources.Buttons(50,50,"Increse R", pygame.Rect(50,50,120,25))
    button_decrese_r = resources.Buttons(150,50,"Decrese R", pygame.Rect(50,85,120,25))
    button_increse_m = resources.Buttons(250,50,"Increse M", pygame.Rect(200,50,120,25))
    button_decrese_m = resources.Buttons(350,50,"Decrese M", pygame.Rect(200,85,120,25))
    button_increse_vx = resources.Buttons(250,50,"+ Vx", pygame.Rect(350,50,50,25))
    button_decrese_vx = resources.Buttons(350,50,"- Vx", pygame.Rect(350,85,50,25))
    button_increse_vy = resources.Buttons(250,50,"+ Vy", pygame.Rect(410,50,50,25))
    button_decrese_vy = resources.Buttons(350,50,"- Vy", pygame.Rect(410,85,50,25))
    add_button = resources.Buttons(350,50,"Add", pygame.Rect(550,50,120,60))
    reset_button = resources.Buttons(350,50,"Reset Praticles", pygame.Rect(850,50,160,25))
    reset_scale_button = resources.Buttons(350,50,"Reset scale", pygame.Rect(1050,50,120,25))
    
    # Text
    text_radius =resources.constants.FONT.render(f'Radius: {resources.constants.ADDED_RADIUS}', True, (240,240,240))
    resources.constants.SCREEN.blit(text_radius, (50, 20))

    text_mass = resources.constants.FONT.render(f'Mass: {resources.constants.ADDED_MASS}', True, (240,240,240))
    resources.constants.SCREEN.blit(text_mass, (200, 20))
        
    text_mass = resources.constants.FONT.render(f'Velocity: {resources.constants.ADDED_VELOCITY}', True, (240,240,240))
    resources.constants.SCREEN.blit(text_mass, (350, 20))
    
    text_num_partciles = resources.constants.FONT.render(f'Number of particles: {resources.constants.NUM_PARTICLES}', True, (240,240,240))
    resources.constants.SCREEN.blit(text_num_partciles, (950, 0))
    
    text_num_partciles = resources.constants.FONT.render(f'Scale: {int(resources.constants.SCALE*100)}%', True, (240,240,240))
    resources.constants.SCREEN.blit(text_num_partciles, (950, 20))
    
    text_num_partciles = resources.constants.FONT.render('Move camera with arrows keys, pause with a space', True, (240,240,240))
    resources.constants.SCREEN.blit(text_num_partciles, (resources.constants.WIDTH // 2 - 200, 0))

    pygame.display.flip()
    resources.constants.CLOCK.tick(60)
pygame.quit()