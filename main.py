import pygame
import random
import math
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Set up the screen
width, height = 1200, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Gravity Simulation")
clock = pygame.time.Clock()
#font 
font = pygame.font.Font('fonts/minecraft_font.ttf', 16)
# Backgorund image 
background_image = pygame.image.load("images/space2.jpg").convert_alpha()
background_image = pygame.transform.scale(background_image, (width, height))

opacity = 100
background_image.set_alpha(opacity)

G = 100
scale = 1.0

class Particle:
    def __init__(self, x, y, mass, color, radius, velocity):
        self.position = pygame.Vector2(x, y)
        self.velocity = velocity
        self.mass = mass
        self.radius = radius
        self.color = color

    def apply_force(self, force):
        acceleration = force / self.mass
        self.velocity += acceleration

    def update(self):
        self.position += self.velocity
    
    def draw_scaled(self, mouse_x, mouse_y):
        scaled_x = int(mouse_x + (self.position.x - mouse_x) * scale)
        scaled_y = int(mouse_y + (self.position.y - mouse_y) * scale)
        pygame.draw.circle(screen, self.color, (scaled_x, scaled_y), int(self.radius * scale))
    
    def apply_gravitational_force(self, other_particle, G):
        dx = abs(self.position.x - other_particle.position.x)
        dy = abs(self.position.y - other_particle.position.y)
        #combined_radius = self.radius + other_particle.radius

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
class Buttons:
    def __init__(self, x_pos, y_pos, text_input, button_rect):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.text_input = text_input
        self.button_rect = button_rect
        self.text = font.render(self.text_input, True, "white")
        self.text_rect = self.text.get_rect(center=(self.button_rect.center))
        self.surface = pygame.Surface(self.button_rect.size, pygame.SRCALPHA)  # Create a surface with transparency
        color = (255, 60, 0, 128)  # Set the color with transparency
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

add_button_statement = False
add_button_statement_put = False

reset_button_statement = False
reset_scale_button_statement = False

# Radius, mass of added particle
added_radius = 20
added_mass = 20

def decrese_radius():
    global added_radius
    if added_radius-1 != 0:
        added_radius -= 1
def increse_radius():
    global added_radius
    added_radius+= 1
def decrese_mass():
    global added_mass
    if added_mass-1 != 0:
        added_mass -= 1
def increse_mass():
    global added_mass
    added_mass += 1
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
                elif add_button.button_rect.collidepoint(event.pos):
                    add_button_statement = True
                elif add_button_statement:
                    add_button_statement_put = True
                elif reset_button.button_rect.collidepoint(event.pos):
                    reset_button_statement = True
                elif reset_scale_button.button_rect.collidepoint(event.pos):
                    reset_scale_button_statement = True

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

    
    # Draw the background image on the screen
    screen.fill((0,0,0))
    screen.blit(background_image, (0, 0))

    if increase_button_stateR:
        increse_radius()
    elif decrease_button_stateR:
        decrese_radius()
    elif increase_button_stateM:
        increse_mass()
    elif decrease_button_stateM:
        decrese_mass()
    elif reset_button_statement:
        reset()
    elif reset_scale_button_statement:
        reset_scale()

    if add_button_statement:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        circle_center = (mouse_x, mouse_y)
        pygame.draw.circle(screen, added_color, circle_center,  added_radius*scale)
    if add_button_statement_put:
        particles.append(Particle(mouse_x, mouse_y, added_mass, added_color, added_radius, pygame.Vector2(0, 0)))
        add_button_statement_put = False
        added_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        num_particles += 1

    for particle in particles:
        particle.update()
        for other_particle in particles:
            if particle != other_particle:
                particle.apply_gravitational_force(other_particle, G)
            particle.draw_scaled(mouse_x,mouse_y)

    # Buttons
    button_increse_r = Buttons(50,50,"Increse r", pygame.Rect(50,50,120,50))
    button_decrese_r = Buttons(150,50,"Decrese r", pygame.Rect(200,50,120,50))
    button_increse_m = Buttons(250,50,"Increse m", pygame.Rect(400,50,120,50))
    button_decrese_m = Buttons(350,50,"Decrese m", pygame.Rect(550,50,120,50))
    add_button = Buttons(350,50,"Add", pygame.Rect(750,50,120,50))
    reset_button = Buttons(350,50,"Reset", pygame.Rect(900,50,120,50))
    reset_scale_button = Buttons(350,50,"Reset scale", pygame.Rect(1050,50,120,50))
    
    # Text
    text_mass = font.render(f'Mass: {added_mass}', True, (240,240,240))
    screen.blit(text_mass, (400, 20))

    text_radius = font.render(f'Radius: {added_radius}', True, (240,240,240))
    screen.blit(text_radius, (50, 20))
    
    text_num_partciles = font.render(f'Number of particles: {num_particles}', True, (240,240,240))
    screen.blit(text_num_partciles, (950, 0))
    
    text_num_partciles = font.render(f'Scale: {int(scale*100)}%', True, (240,240,240))
    screen.blit(text_num_partciles, (950, 20))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()