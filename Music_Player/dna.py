import pygame
import math
import random

pygame.init()
W, H = 900, 600
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Digital DNA Lab")
clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas", 26)

particles = [
    [random.randrange(W), random.randrange(H), random.randint(1, 3)]
    for _ in range(100)
]

angle = 0
running = True

while running:
    clock.tick(60)
    angle += 0.035

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((5, 8, 25))

    # Background particles
    for p in particles:
        p[1] -= p[2] * 0.4
        if p[1] < 0:
            p[1] = H
            p[0] = random.randrange(W)

        pygame.draw.circle(screen, (40, 90, 150),
                           (p[0], int(p[1])), p[2])

    center_x = W // 2

    # Two twisting DNA strands
    for i in range(55):
        y = 90 + i * 8
        phase = i * 0.20 + angle
        x1 = center_x + int(140 * math.sin(phase))
        x2 = center_x + int(140 * math.sin(phase + math.pi))

        # Connecting DNA pairs
        pygame.draw.line(screen, (80, 100, 160),
                         (x1, y), (x2, y), 2)

        pygame.draw.circle(screen, (0, 230, 255), (x1, y), 7)
        pygame.draw.circle(screen, (255, 70, 180), (x2, y), 7)

    title = font.render("DNA DOUBLE HELIX", True, (100, 255, 255))
    screen.blit(title, (300, 25))

    subtitle = pygame.font.SysFont("consolas", 16).render(
        "GENETIC STRUCTURE SIMULATION", True, (170, 180, 210)
    )
    screen.blit(subtitle, (295, 565))

    pygame.display.flip()

pygame.quit()