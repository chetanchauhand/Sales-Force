import pygame
import math
import random

pygame.init()
W, H = 900, 600
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Magic Portal")
clock = pygame.time.Clock()

cx, cy = W // 2, H // 2
particles = []
angle = 0

for _ in range(220):
    particles.append({
        "a": random.random() * math.tau,
        "r": random.randint(65, 190),
        "speed": random.uniform(0.005, 0.035),
        "size": random.randint(2, 5)
    })

running = True
while running:
    clock.tick(60)
    angle += 0.025

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Portal follows the mouse
    mx, my = pygame.mouse.get_pos()
    cx += (mx - cx) * 0.035
    cy += (my - cy) * 0.035

    screen.fill((5, 3, 20))

    # Outer energy rings
    for i in range(8):
        radius = 80 + i * 13 + int(4 * math.sin(angle + i))
        color = (60 + i * 10, 40, 255)
        pygame.draw.ellipse(
            screen, color,
            (int(cx - radius), int(cy - radius * 1.35),
             radius * 2, int(radius * 2.7)), 2
        )

    # Rotating particles
    for p in particles:
        p["a"] += p["speed"]
        radius = p["r"] + 8 * math.sin(angle * 2 + p["a"])

        x = int(cx + math.cos(p["a"]) * radius)
        y = int(cy + math.sin(p["a"]) * radius * 1.3)

        pygame.draw.circle(
            screen, (100, 100, 255),
            (x, y), p["size"] + 2
        )
        pygame.draw.circle(
            screen, (180, 220, 255),
            (x, y), p["size"]
        )

    # Portal center
    pygame.draw.ellipse(
        screen, (30, 10, 100),
        (int(cx - 65), int(cy - 90), 130, 180)
    )
    pygame.draw.ellipse(
        screen, (0, 230, 255),
        (int(cx - 65), int(cy - 90), 130, 180), 4
    )

    font = pygame.font.SysFont("consolas", 24)
    text = font.render("MAGIC PORTAL", True, (180, 220, 255))
    screen.blit(text, (20, 20))

    pygame.display.flip()

pygame.quit()