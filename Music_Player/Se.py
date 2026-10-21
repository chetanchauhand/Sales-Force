import pygame
import random

pygame.init()
W, H = 900, 550
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Shadow Warrior")
clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas", 24)

player = pygame.Rect(100, 390, 38, 65)
enemies = [pygame.Rect(600, 400, 35, 55)]
health = 100
score = 0
velocity_y = 0
attacking = 0
spawn_timer = 0
running = True

while running:
    clock.tick(60)
    spawn_timer += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_SPACE and player.bottom >= 455:
                velocity_y = -14
            if event.key == pygame.K_j:
                attacking = 12

    keys = pygame.key.get_pressed()
    player.x += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * 5
    player.x = max(0, min(W - player.width, player.x))

    velocity_y += 0.7
    player.y += int(velocity_y)

    if player.bottom >= 455:
        player.bottom = 455
        velocity_y = 0

    if attacking > 0:
        attacking -= 1

    if spawn_timer > 100 and len(enemies) < 5:
        enemies.append(pygame.Rect(
            random.choice([0, W - 35]), 400, 35, 55
        ))
        spawn_timer = 0

    screen.fill((12, 10, 28))
    pygame.draw.rect(screen, (45, 35, 60), (0, 455, W, 95))
    pygame.draw.line(screen, (150, 50, 255), (0, 455), (W, 455), 3)

    # Player
    pygame.draw.circle(screen, (220, 190, 170),
                       (player.centerx, player.y + 12), 13)
    pygame.draw.rect(screen, (80, 60, 180),
                     (player.x, player.y + 27, 38, 38))

    # Sword attack
    if attacking > 0:
        sword = pygame.Rect(player.right, player.y + 20, 55, 10)
        pygame.draw.rect(screen, (0, 255, 255), sword)

    for enemy in enemies[:]:
        if enemy.centerx < player.centerx:
            enemy.x += 2
        elif enemy.centerx > player.centerx:
            enemy.x -= 2

        pygame.draw.rect(screen, (210, 45, 70), enemy)
        pygame.draw.circle(screen, (255, 170, 140),
                           (enemy.centerx, enemy.y - 7), 12)

        if attacking > 0:
            attack_area = pygame.Rect(
                player.x - 55, player.y, player.width + 110, player.height
            )
            if attack_area.colliderect(enemy):
                enemies.remove(enemy)
                score += 1
                continue

        if player.colliderect(enemy):
            health -= 1
            if health <= 0:
                health = 0

    pygame.draw.rect(screen, (60, 60, 60), (20, 20, 205, 24))
    pygame.draw.rect(screen, (30, 230, 90), (20, 20, health * 2, 24))
    screen.blit(font.render(f"Health: {health}  Score: {score}",
                           True, (255, 255, 255)), (20, 55))
    screen.blit(font.render("Arrows: Move | SPACE: Jump | J: Attack",
                           True, (255, 255, 100)), (20, 510))

    if health <= 0:
        screen.blit(font.render("GAME OVER - Close window to exit",
                               True, (255, 50, 50)), (280, 250))

    pygame.display.flip()

pygame.quit()