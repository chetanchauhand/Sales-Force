
import pygame
import random
import math

pygame.init()
W, H = 1000, 650
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("DRAGON FIRE")
clock = pygame.time.Clock()

particles = []
running = True
frame = 0

while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

    screen.fill((12, 5, 20))
    frame += 1

    # Ground
    pygame.draw.ellipse(screen, (45, 12, 25),
                        (60, 480, 880, 110))

    # Dragon body
    pygame.draw.ellipse(screen, (30, 35, 55),
                        (260, 330, 350, 150))
    pygame.draw.circle(screen, (30, 35, 55),
                       (600, 330), 85)

    # Neck and head
    pygame.draw.polygon(screen, (40, 45, 65), [
        (540, 350), (620, 240), (720, 260),
        (760, 305), (675, 330), (625, 410)
    ])
    pygame.draw.polygon(screen, (60, 65, 90), [
        (615, 260), (630, 190), (650, 245)
    ])
    pygame.draw.polygon(screen, (60, 65, 90), [
        (670, 255), (710, 195), (700, 275)
    ])

    # Wings
    pygame.draw.polygon(screen, (35, 25, 65), [
        (450, 355), (300, 150), (345, 345),
        (210, 235), (330, 420)
    ])
    pygame.draw.polygon(screen, (90, 30, 100), [
        (450, 355), (300, 150), (345, 345),
        (210, 235), (330, 420)
    ], 3)

    # Legs and tail
    pygame.draw.line(screen, (35, 40, 60),
                     (350, 420), (300, 500), 24)
    pygame.draw.line(screen, (35, 40, 60),
                     (510, 425), (555, 500), 24)
    pygame.draw.lines(screen, (40, 45, 65), False, [
        (300, 390), (220, 440), (130, 420)
    ], 25)

    # Eye
    pygame.draw.circle(screen, (255, 30, 0),
                       (680, 275), 10)
    pygame.draw.circle(screen, (255, 220, 80),
                       (682, 275), 4)

    # Fire particles from dragon mouth
    for _ in range(8):
        particles.append([
            745, 310,
            random.uniform(3, 8),
            random.uniform(-2.8, -0.8),
            random.randint(15, 35)
        ])

    for p in particles[:]:
        x, y, vx, vy, life = p
        x += vx
        y += vy + random.uniform(-1, 1)
        life -= 1
        p[:] = [x, y, vx, vy, life]

        if life <= 0:
            particles.remove(p)
            continue

        radius = max(1, life // 5)
        color = random.choice([
            (255, 35, 0), (255, 100, 0),
            (255, 210, 20), (255, 245, 150)
        ])
        pygame.draw.circle(screen, color,
                           (int(x), int(y)), radius)

    font = pygame.font.SysFont("consolas", 25)
    screen.blit(font.render("DRAGON FIRE", True,
                            (255, 90, 30)), (30, 25))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
