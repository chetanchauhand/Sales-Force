
import pygame
import random
import math

pygame.init()

WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("NEON GALAXY")

clock = pygame.time.Clock()
center = (WIDTH // 2, HEIGHT // 2)

stars = []

for _ in range(700):
    angle = random.uniform(0, math.tau)
    radius = random.uniform(10, 340)
    speed = random.uniform(0.15, 0.8)
    size = random.choice([1, 1, 2, 3])

    stars.append([angle, radius, speed, size])

running = True
rotation = 0

while running:
    screen.fill((3, 4, 18))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    rotation += 0.003

    # Glowing galaxy core
    for r in range(100, 5, -5):
        glow = max(0, 150 - r)
        pygame.draw.circle(
            screen,
            (glow // 3, 0, glow),
            center,
            r,
            2
        )

    # Spiral stars
    for star in stars:
        angle, radius, speed, size = star
        angle += speed * 0.008 + rotation
        star[0] = angle

        spiral_angle = angle + radius * 0.018

        x = center[0] + math.cos(spiral_angle) * radius
        y = center[1] + math.sin(spiral_angle) * radius * 0.62

        color = (
            random.randint(70, 120),
            random.randint(100, 190),
            255
        )

        pygame.draw.circle(
            screen, color,
            (int(x), int(y)), size
        )

    # Central energy sphere
    pygame.draw.circle(screen, (70, 160, 255), center, 9)
    pygame.draw.circle(screen, (220, 240, 255), center, 4)

    font = pygame.font.SysFont("consolas", 22)
    label = font.render("NEON GALAXY // LIVE", True, (0, 220, 255))
    screen.blit(label, (25, 25))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
