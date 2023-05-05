import pygame
import random
import math
from pygame.locals import *

pygame.init()

width, height = 1200, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Gravity Simulation")
clock = pygame.time.Clock()
clock.tick(60)

#font 
font = pygame.font.Font('fonts/minecraft_font.ttf', 16)

# Backgorund image 
#background_image = pygame.image.load("images/space2.jpg").convert_alpha()
#background_image = pygame.transform.scale(background_image, (width, height))

opacity = 100
#background_image.set_alpha(opacity)
G = 100
scale = 1.0

class Particle:
    def __init__(self, x, y, mass, color, radius, velocity):
        self.position = pygame.Vector2(x, y)
        self.velocity = velocity
        self.mass = mass
        self.radius = radius
        self.color = color
        self.stats_text = None
        self.selected = None
    def apply_force(self, force):
        acceleration = force / self.mass
        self.velocity += acceleration
    def update(self):
        self.position += self.velocity
    
    def draw_scaled(self, mouse_x, mouse_y):
        scaled_x = int(mouse_x + (self.position.x - mouse_x) * scale)
        scaled_y = int(mouse_y + (self.position.y - mouse_y) * scale)
        circle_center = (scaled_x, scaled_y)
        pygame.draw.circle(screen, self.color, circle_center, int(self.radius * scale))

        # Render and position the statistics text
        if self.selected:
            stats_lines = [
                f"Mass: {self.mass}",
                f"Radius: {self.radius}",
                f"Velocity: {round(self.velocity.x, 2), round(self.velocity.y, 2)}"
            ]
            line_height = 20  
            text_y = scaled_y + int(self.radius * scale) + 10  
            for i, line in enumerate(stats_lines):
                stats_text = font.render(line, True, (255, 255, 255))
                stats_text_rect = stats_text.get_rect(center=(scaled_x, text_y + i * line_height))
                screen.blit(stats_text, stats_text_rect)

    def apply_gravitational_force(self, other_particle, G):
        dx = abs(self.position.x - other_particle.position.x)
        dy = abs(self.position.y - other_particle.position.y)

        if dx < self.radius*2 or dy < self.radius*2 :
            pass
        else:
            try:
                r = math.sqrt(dx**2 + dy**2)
                a = G * other_particle.mass / r**2
                theta = math.asin(dy / r)

                if self.position.y  > other_particle.position.y:
                    self.apply_force(pygame.Vector2(0, -math.sin(theta) * a))
                else:
                    self.apply_force(pygame.Vector2(0, math.sin(theta) * a))

                if self.position.x > other_particle.position.x:
                    self.apply_force(pygame.Vector2(-math.cos(theta) * a, 0))
                else:
                    self.apply_force(pygame.Vector2(math.cos(theta) * a, 0))
            except ZeroDivisionError:
                pass
    def is_clicked(self, mouse_pos):
        return self.position.distance_to(pygame.Vector2(*mouse_pos)) <= self.radius
    
class Buttons:
    def __init__(self, x_pos, y_pos, text_input, button_rect):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.text_input = text_input
        self.button_rect = button_rect
        self.text = font.render(self.text_input, True, "white")
        self.text_rect = self.text.get_rect(center=(self.button_rect.center))
        self.surface = pygame.Surface(self.button_rect.size, pygame.SRCALPHA)  # Create a surface with transparency
        color = (100, 80, 90, 128)  # Set the color with transparency
        pygame.draw.rect(self.surface, color, (0, 0, *self.button_rect.size))  # Draw the rectangle on the surface
        screen.blit(self.surface, self.button_rect)  # Blit the surface onto the screen
        screen.blit(self.text, self.text_rect)
                 
# Create a list of particles
particles = []
num_particles = 30

# Generate random particles
for i in range(num_particles):
    if i == 0:
        x = width // 2
        y = height // 2
        mass = 60
        particles.append(Particle(x, y, mass, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), random.randint(30, 30), pygame.Vector2(0, 0)))
    else:
        x = random.randint(0, width)
        y = random.randint(0, height)
        mass = random.uniform(1, 10)
        mass = 5
        particles.append(Particle(x, y, mass, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), random.randint(0, 5), pygame.Vector2(0, 0)))

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

# Initial values 
added_radius = 20
added_mass = 20
added_velocity = pygame.Vector2(0, 0)

def decrease_radius():
    global added_radius
    if added_radius-1 != 0:
        added_radius -= 1
def increase_radius():
    global added_radius
    added_radius+= 1
def decrease_mass():
    global added_mass
    if added_mass-1 != 0:
        added_mass -= 1
def increase_mass():
    global added_mass
    added_mass += 1
def decrease_velocity_x():
    global added_velocity
    if not add_button_statement_put:
        added_velocity.x -= 0.05
def increase_velocity_x():
    global added_velocity
    if not add_button_statement_put:
        added_velocity.x += 0.05
def decrease_velocity_y():
    global added_velocity
    if not add_button_statement_put:
        added_velocity.y -= 0.05
def increase_velocity_y():
    global added_velocity
    if not add_button_statement_put:
        added_velocity.y += 0.05
def reset():
    global num_particles, particles, reset_button_statement 
    num_particles = 0
    particles = []
    reset_button_statement = False
def reset_scale():
    global scale, reset_scale_button_statement  
    scale = 1
    reset_scale_button_statement = False


added_color = (255,255,255)
running = True
mouse_x, mouse_y = pygame.mouse.get_pos()
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
                for particle in particles:
                    scaled_x = int(mouse_x + (particle.position.x - mouse_x) * scale)
                    scaled_y = int(mouse_y + (particle.position.y - mouse_y) * scale)
                    distance = math.sqrt((event.pos[0] - scaled_x)**2 + (event.pos[1] - scaled_y)**2)
                    if distance <= particle.radius * scale:
                        particle.selected = not particle.selected

            if event.button == 3: # Right click
                if add_button_statement:
                    add_button_statement = False
            elif event.button == 4:  # Scroll Up
                scale += 0.1
                mouse_x, mouse_y = pygame.mouse.get_pos()
                
            elif event.button == 5:  # Scroll Down
                if scale - 0.1 > 0:
                    scale -= 0.1
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                
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
    screen.fill((20,20,40))
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
        reset()
    elif reset_scale_button_statement:
        reset_scale()

    if add_button_statement:
        mouse_xd, mouse_yd = pygame.mouse.get_pos()
        scaled_mouse_x = int(mouse_x + (mouse_xd - mouse_x) * scale)
        scaled_mouse_y = int(mouse_y + (mouse_yd - mouse_y) * scale)
        circle_center = (scaled_mouse_x, scaled_mouse_y)
        circle_radius = int(added_radius * scale)
        pygame.draw.circle(
            screen, 
            added_color, 
            circle_center, 
            circle_radius
            )

    if add_button_statement_put:
        particle_velocity = added_velocity.copy()
        particles.append(
            Particle(
                mouse_xd,
                mouse_yd,
                added_mass,
                added_color,
                added_radius,
                particle_velocity
            )
        )
        add_button_statement_put = False
        added_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        num_particles += 1

    # Sort in case bigger particles do not cover smaller ones 
    particles = sorted(particles, key=lambda x: x.radius, reverse=True)
    for particle in particles:
        if move_particles:
            particle.position += move_direction * scale
        elif pause:
            pass
        else:
            particle.update()
        
            for other_particle in particles:
                if particle != other_particle:
                    particle.apply_gravitational_force(other_particle, G)
        particle.draw_scaled(mouse_x, mouse_y)

    # Buttons
    button_increse_r = Buttons(50,50,"Increse R", pygame.Rect(50,50,120,25))
    button_decrese_r = Buttons(150,50,"Decrese R", pygame.Rect(50,85,120,25))
    button_increse_m = Buttons(250,50,"Increse M", pygame.Rect(200,50,120,25))
    button_decrese_m = Buttons(350,50,"Decrese M", pygame.Rect(200,85,120,25))
    button_increse_vx = Buttons(250,50,"+ Vx", pygame.Rect(350,50,50,25))
    button_decrese_vx = Buttons(350,50,"- Vx", pygame.Rect(350,85,50,25))
    button_increse_vy = Buttons(250,50,"+ Vy", pygame.Rect(410,50,50,25))
    button_decrese_vy = Buttons(350,50,"- Vy", pygame.Rect(410,85,50,25))
    add_button = Buttons(350,50,"Add", pygame.Rect(550,50,120,60))
    reset_button = Buttons(350,50,"Reset Praticles", pygame.Rect(850,50,160,25))
    reset_scale_button = Buttons(350,50,"Reset scale", pygame.Rect(1050,50,120,25))
    
    # Text
    text_radius = font.render(f'Radius: {added_radius}', True, (240,240,240))
    screen.blit(text_radius, (50, 20))

    text_mass = font.render(f'Mass: {added_mass}', True, (240,240,240))
    screen.blit(text_mass, (200, 20))
        
    text_mass = font.render(f'Velocity: {added_velocity}', True, (240,240,240))
    screen.blit(text_mass, (350, 20))
    
    text_num_partciles = font.render(f'Number of particles: {num_particles}', True, (240,240,240))
    screen.blit(text_num_partciles, (950, 0))
    
    text_num_partciles = font.render(f'Scale: {int(scale*100)}%', True, (240,240,240))
    screen.blit(text_num_partciles, (950, 20))
    
    text_num_partciles = font.render('Move camera with arrows keys, pause with a space', True, (240,240,240))
    screen.blit(text_num_partciles, (width // 2 - 200, 0))

    pygame.display.flip()

pygame.quit()