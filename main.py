import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the screen
width, height = 1200, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Gravity Simulation")
clock = pygame.time.Clock()
#font 
font = pygame.font.SysFont(None, 24)
mouse_x, mouse_y = 0, 0
G = 1

class Particle:
    def __init__(self, x, y, mass, color, radius):
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.mass = mass
        self.radius = radius
        self.color = color

    def apply_force(self, force):
        acceleration = force / self.mass
        self.velocity += acceleration

    def update(self):
        self.position += self.velocity

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.position.x), int(self.position.y)), self.radius)
        
# Create a list of particles
particles = []
num_particles = 50

# Generate random particles
for i in range(num_particles):
    if i == 0:
        x = width // 2
        y = height // 2
        mass = 30
        particles.append(Particle(x, y, mass, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), 10))
    else:
        x = random.randint(0, width)
        y = random.randint(0, height)
        mass = random.uniform(1, 10)
        particles.append(Particle(x, y, mass, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), 10))

decrese_buttonR = pygame.Rect(50,50,100,50)
increse_buttonR = pygame.Rect(150,50,100,50)

decrese_buttonM = pygame.Rect(250,50,100,50)
increse_buttonM = pygame.Rect(350,50,100,50)

add_button = pygame.Rect(650,50,100,50)

# Initialize button states
increase_button_stateR = False
decrease_button_stateR = False

increase_button_stateM = False
decrease_button_stateM = False

add_button_statement = False
add_button_statement_put = False


def decrese_radius():
    if particles[0].radius-1 != 0:
        particles[0].radius -= 1
    print(particles[0].radius)
def increse_radius():
    particles[0].radius += 1
    print(particles[0].radius)
def decrese_mass():
    if particles[0].mass-1 != 0:
        particles[0].mass -= 1
    print(particles[0].mass)
def increse_mass():
    particles[0].mass += 1
    print(particles[0].mass)

added_color = (255,255,255)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # Left click
                # Check if the mouse click is inside the buttons
                if increse_buttonR.collidepoint(event.pos):
                    increase_button_stateR = True
                elif decrese_buttonR.collidepoint(event.pos):
                    decrease_button_stateR = True
                elif increse_buttonM.collidepoint(event.pos):
                    increase_button_stateM = True
                elif decrese_buttonM.collidepoint(event.pos):
                    decrease_button_stateM = True
                elif add_button.collidepoint(event.pos):
                    add_button_statement = True
                elif add_button_statement:
                    add_button_statement_put = True
            if event.button == 3: # Right click
                if add_button_statement:
                    add_button_statement = False
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                # Reset button states
                increase_button_stateR = False
                decrease_button_stateR = False
                increase_button_stateM = False
                decrease_button_stateM = False

    screen.fill((0, 0, 0))  # Fill the background with white color
    
    # Buttons
    pygame.draw.rect(screen, (255,0,0), decrese_buttonR)
    decrese_textR = font.render("decrese r", True, (0,0,0))
    decrese__text_rectR = decrese_textR.get_rect(center=decrese_buttonR.center)
    screen.blit(decrese_textR, decrese__text_rectR)
    pygame.draw.rect(screen, (255,0,0), increse_buttonR)
    increase_textR = font.render("Increase r", True, (0,0,0))
    increase_text_rectR = increase_textR.get_rect(center=increse_buttonR.center)
    screen.blit(increase_textR, increase_text_rectR)
    pygame.draw.rect(screen, (0,255,0), decrese_buttonM)
    decrese_textM = font.render("decrese m", True, (0,0,0))
    decrese__text_rectM = decrese_textM.get_rect(center=decrese_buttonM.center)
    screen.blit(decrese_textM, decrese__text_rectM)
    pygame.draw.rect(screen, (0,255,0), increse_buttonM)
    increase_textM = font.render("Increase m", True, (0,0,0))
    increase_text_rectM = increase_textM.get_rect(center=increse_buttonM.center)
    screen.blit(increase_textM, increase_text_rectM)
    pygame.draw.rect(screen, (0,255,0), add_button)
    text = font.render("Add", True, (0,0,0))
    text_rect = text.get_rect(center=add_button.center)
    screen.blit(text, text_rect)
    
    
    if increase_button_stateR:
        increse_radius()
    elif decrease_button_stateR:
        decrese_radius()
    elif increase_button_stateM:
        increse_mass()
    elif decrease_button_stateM:
        decrese_mass()
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if add_button_statement:
        circle_center = (mouse_x, mouse_y)
        pygame.draw.circle(screen, added_color, circle_center, 20)
    if add_button_statement_put:
        mass = random.uniform(1, 10)
        particles.append(Particle(mouse_x, mouse_y, mass, added_color, 20))
        add_button_statement_put = False
        added_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


    for i in range(len(particles)):
        for j in range(i+1, len(particles)):
            particle1 = particles[i]
            particle2 = particles[j]
            distance = particle2.position.distance_to(particle1.position)
            if distance < particle1.radius + particle2.radius:
                continue

            distance_vec = particle2.position - particle1.position
            magnitude = distance_vec.length()
            direction = distance_vec.normalize()
            gravitational_force = G * (particle2.mass * particle1.mass) / (magnitude ** 2)
            force = direction * gravitational_force

            particle1.apply_force(force)
            particle2.apply_force(-force)

    for particle in particles:
        particle.update()
        particle.draw()

    pygame.display.flip()
    clock.tick(120)

pygame.quit()
