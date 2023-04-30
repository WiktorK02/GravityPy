import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the screen
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Gravity Simulation")
clock = pygame.time.Clock()

class Particle:
    def __init__(self, x, y, mass, color):
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.mass = mass
        self.radius = mass
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
num_particles = 100

# Generate random particles
for i in range(num_particles):
    if i == 1:
        x = width // 2
        y = height // 2
        mass = 30
        particles.append(Particle(x, y, mass, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))))
    else:
        x = random.randint(0, width)
        y = random.randint(0, height)
        mass = random.uniform(1, 10)
        particles.append(Particle(x, y, mass, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))))

G = 1
running = True
while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))  # Fill the background with white color

    for i in range(num_particles):
        for j in range(i+1, num_particles):
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
