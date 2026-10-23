
import pygame
import random
import math

pygame.init()
W, H = 1000, 700
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("BLACK HOLE SIMULATOR")
clock = pygame.time.Clock()

cx, cy = W // 2, H // 2
particles = []

for _ in range(850):
    particles.append([
        random.uniform(45, 330),
        random.uniform(0, math.tau),
        random.uniform(0.003, 0.018),
        random.randint(1, 3)
    ])

stars = [(random.randrange(W), random.randrange(H))
         for _ in range(250)]

running = True
angle_offset = 0

while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

    screen.fill((2, 3, 15))

    for x, y in stars:
        screen.set_at((x, y), (90, 100, 150))

    angle_offset += 0.01

    # Accretion disk
    for radius in range(320, 45, -3):
        col = (max(20, 150 - radius // 3),
               max(5, 75 - radius // 5), 255)
        pygame.draw.ellipse(
            screen, col,
            (cx-radius, cy-radius*0.45,
             radius*2, radius*0.9), 1
        )

    # Orbiting glowing particles
    for p in particles:
        r, a, speed, size = p
        a += speed * (350 / max(r, 40))
        p[1] = a

        x = cx + math.cos(a + angle_offset) * r
        y = cy + math.sin(a + angle_offset) * r * 0.43

        color = random.choice([
            (255, 90, 20), (255, 180, 50),
            (100, 170, 255), (220, 80, 255)
        ])
        pygame.draw.circle(screen, color,
                           (int(x), int(y)), size)

    # Event horizon and photon ring
    pygame.draw.ellipse(
        screen, (255, 180, 60),
        (cx-65, cy-30, 130, 60), 3
    )
    pygame.draw.circle(screen, (0, 0, 0), (cx, cy), 42)
    pygame.draw.circle(screen, (120, 170, 255),
                       (cx, cy), 44, 2)

    font = pygame.font.SysFont("consolas", 22)
    screen.blit(font.render("EVENT HORIZON", True,
                            (100, 210, 255)), (25, 25))
    screen.blit(font.render("PARTICLE ORBITS: ACTIVE", True,
                            (255, 140, 50)), (25, 55))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
