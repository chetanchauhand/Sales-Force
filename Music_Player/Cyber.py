import pygame
import random

pygame.init()
W, H = 900, 600
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Cyberpunk City")
clock = pygame.time.Clock()

buildings = []
for x in range(0, W, 90):
    buildings.append(
        (x, random.randint(180, 340), random.choice([
            (0, 255, 255), (255, 0, 180), (120, 100, 255)
        ]))
    )

rain = [[random.randrange(W), random.randrange(H)]
        for _ in range(150)]
cars = [[random.randrange(W), random.choice([470, 520]),
         random.choice([-1, 1])] for _ in range(6)]

tick = 0
font = pygame.font.SysFont("consolas", 24)
running = True

while running:
    clock.tick(60)
    tick += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((8, 7, 25))

    # Buildings
    for x, height, neon in buildings:
        pygame.draw.rect(screen, (20, 20, 45),
                         (x, H - height, 82, height))

        for wx in range(x + 10, x + 75, 20):
            for wy in range(H - height + 15, H - 30, 30):
                pygame.draw.rect(screen, neon, (wx, wy, 5, 9))

    # Road
    pygame.draw.rect(screen, (25, 25, 35), (0, 440, W, 160))
    pygame.draw.line(screen, (255, 0, 180), (0, 440), (W, 440), 3)

    # Moving cars
    for car in cars:
        car[0] += car[2] * 4
        if car[0] > W + 60:
            car[0] = -60
        if car[0] < -60:
            car[0] = W + 60

        pygame.draw.rect(screen, (30, 220, 255),
                         (car[0], car[1], 55, 22))
        pygame.draw.circle(screen, (5, 5, 5), (int(car[0] + 12), car[1] + 22), 7)
        pygame.draw.circle(screen, (5, 5, 5), (int(car[0] + 43), car[1] + 22), 7)

    # Rain
    for drop in rain:
        drop[1] += 8
        if drop[1] > H:
            drop[0], drop[1] = random.randrange(W), 0
        pygame.draw.line(screen, (70, 130, 190),
                         drop, (drop[0] - 3, drop[1] + 8), 1)

    # Occasional lightning flash
    if tick % 420 < 3:
        screen.fill((100, 100, 130))

    screen.blit(font.render("NEON CITY | NIGHT DRIVE",
                            True, (0, 255, 255)), (20, 20))
    pygame.display.flip()

pygame.quit()