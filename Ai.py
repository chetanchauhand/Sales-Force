
import pygame
import math
import random

pygame.init()
W, H = 1000, 700
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("AI HOLOGRAM")
clock = pygame.time.Clock()

font = pygame.font.SysFont("consolas", 22)
small = pygame.font.SysFont("consolas", 15)

running = True
t = 0

while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

    screen.fill((2, 10, 24))
    t += 1

    # Digital grid
    for x in range(0, W, 50):
        pygame.draw.line(screen, (8, 35, 55),
                         (x, 0), (x, H))
    for y in range(0, H, 50):
        pygame.draw.line(screen, (8, 35, 55),
                         (0, y), (W, y))

    # Robot head outline
    pulse = int(130 + 60 * math.sin(t * 0.05))
    cyan = (20, pulse, 255)

    pygame.draw.rect(screen, cyan,
                     (340, 160, 320, 350), 3,
                     border_radius=45)
    pygame.draw.rect(screen, (10, 50, 85),
                     (365, 190, 270, 290), 2,
                     border_radius=35)

    # Eyes
    eye_y = 285 + int(5 * math.sin(t * 0.08))
    for ex in (425, 575):
        pygame.draw.ellipse(screen, (0, 80, 140),
                            (ex-32, eye_y-22, 64, 44))
        pygame.draw.ellipse(screen, (0, 220, 255),
                            (ex-25, eye_y-15, 50, 30), 3)
        pygame.draw.circle(screen, (220, 255, 255),
                           (ex, eye_y), 8)

    # Mouth equalizer
    for i in range(9):
        h = random.randint(8, 45)
        pygame.draw.rect(screen, (0, 220, 255),
                         (405 + i*24, 405-h//2, 12, h))

    # Scanning laser
    laser_y = 170 + (t * 3) % 330
    pygame.draw.line(screen, (255, 0, 160),
                     (350, laser_y), (650, laser_y), 2)

    # Floating data points
    for i in range(35):
        x = int(50 + (i*83 + t*2) % 900)
        y = int(60 + (i*47) % 560)
        pygame.draw.circle(screen, (0, 120, 180),
                           (x, y), 2)

    screen.blit(font.render("AI CORE // ONLINE", True,
                            cyan), (30, 25))
    screen.blit(small.render("NEURAL SYSTEM ACTIVE", True,
                             (0, 200, 230)), (30, 60))
    screen.blit(small.render("SCANNING...", True,
                             (255, 40, 170)), (800, 620))

    pygame.display.flip()
    clock.tick(40)

pygame.quit()
