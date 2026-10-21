import pygame
import random
import math

pygame.init()

W, H = 900, 600
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Space Explorer")
clock = pygame.time.Clock()

stars = [
    [random.randrange(W), random.randrange(H), random.randint(1, 3)]
    for _ in range(120)
]

ship_x, ship_y = W // 2, H - 100
lasers = []
asteroids = [
    [random.randrange(W), random.randrange(-600, 0), random.randint(15, 30)]
    for _ in range(12)
]

score = 0
font = pygame.font.SysFont("consolas", 22)
running = True

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                lasers.append([ship_x, ship_y - 20])

    keys = pygame.key.get_pressed()
    ship_x += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * 6
    ship_y += (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * 6
    ship_x = max(20, min(W - 20, ship_x))
    ship_y = max(30, min(H - 30, ship_y))

    screen.fill((5, 5, 25))

    for star in stars:
        star[1] += star[2]
        if star[1] > H:
            star[0], star[1] = random.randrange(W), 0
        pygame.draw.circle(screen, (180, 210, 255),
                           (star[0], star[1]), star[2] // 2 + 1)

    for a in asteroids[:]:
        a[1] += 3
        pygame.draw.circle(screen, (130, 120, 145),
                           (a[0], int(a[1])), a[2])

        if a[1] > H + 30:
            a[0], a[1] = random.randrange(W), random.randrange(-200, -30)

    for laser in lasers[:]:
        laser[1] -= 10
        pygame.draw.rect(screen, (0, 255, 255),
                         (laser[0] - 2, laser[1], 4, 18))

        if laser[1] < 0:
            lasers.remove(laser)
            continue

        for a in asteroids[:]:
            if math.hypot(laser[0] - a[0], laser[1] - a[1]) < a[2]:
                if laser in lasers:
                    lasers.remove(laser)
                a[0], a[1] = random.randrange(W), -30
                score += 1
                break

    # Spaceship
    pygame.draw.polygon(
        screen, (0, 220, 255),
        [(ship_x, ship_y - 25),
         (ship_x - 20, ship_y + 20),
         (ship_x, ship_y + 10),
         (ship_x + 20, ship_y + 20)]
    )

    screen.blit(font.render(f"Score: {score} | SPACE: Shoot",
                            True, (255, 255, 255)), (20, 20))

    pygame.display.flip()

pygame.quit()