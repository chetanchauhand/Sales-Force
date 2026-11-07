
import pygame
import math
import random
import sys

pygame.init()

WIDTH, HEIGHT = 1000, 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Giant Rasgulla Animation")

clock = pygame.time.Clock()

# Colors
BG = (30, 18, 22)
WHITE = (255, 250, 235)
CREAM = (255, 235, 195)
SHADOW = (120, 75, 65)
SYRUP = (255, 170, 65)
GOLD = (255, 210, 120)

font = pygame.font.SysFont("Arial", 36, bold=True)
small = pygame.font.SysFont("Arial", 20)

center_x = WIDTH // 2
base_y = 420

# Animation variables
time = 0
syrup_drops = []

for i in range(35):
    syrup_drops.append([
        random.randint(0, WIDTH),
        random.randint(450, HEIGHT),
        random.uniform(1, 3),
        random.randint(2, 5)
    ])


def draw_rasgulla(surface, x, y, radius):

    # Shadow
    pygame.draw.ellipse(
        surface,
        (10, 7, 12),
        (x-radius, y+radius-5, radius*2, 35)
    )

    # Main sphere
    pygame.draw.circle(
        surface,
        SHADOW,
        (x+5, y+8),
        radius
    )

    pygame.draw.circle(
        surface,
        CREAM,
        (x, y),
        radius
    )

    # Soft white highlight
    pygame.draw.circle(
        surface,
        WHITE,
        (x-35, y-35),
        int(radius*0.72)
    )

    # Shading
    shade = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)

    pygame.draw.ellipse(
        shade,
        (190, 130, 100, 65),
        (radius*0.8, radius*0.8, radius, radius*0.9)
    )

    surface.blit(shade, (x-radius, y-radius))

    # Texture dots
    random.seed(10)

    for i in range(100):
        angle = random.uniform(0, math.pi*2)
        distance = random.uniform(0, radius*0.85)

        px = x + math.cos(angle)*distance
        py = y + math.sin(angle)*distance

        pygame.draw.circle(
            surface,
            (225, 205, 175),
            (int(px), int(py)),
            2
        )

    # Shine
    pygame.draw.ellipse(
        surface,
        (255, 255, 255),
        (x-70, y-85, 55, 25)
    )


running = True

while running:

    screen.fill(BG)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            if event.key == pygame.K_SPACE:
                time = 0

    time += 0.04

    # Decorative background
    for i in range(10):
        pygame.draw.circle(
            screen,
            (48, 29, 34),
            (center_x, 320),
            200 + i*25,
            1
        )

    # Bowl
    pygame.draw.ellipse(
        screen,
        (130, 65, 35),
        (170, 480, 660, 160)
    )

    pygame.draw.ellipse(
        screen,
        SYRUP,
        (185, 475, 630, 125)
    )
    # Syrup waves
    wave_points = []

    for x in range(190, 810, 5):
        y = 530 + math.sin(x*0.025 + time)*8
        wave_points.append((x, y))

    pygame.draw.lines(
        screen,
        GOLD,
        False,
        wave_points,
        4
    )

    # Giant rasgulla bouncing
    bounce = math.sin(time*2)*12
    y = base_y + bounce

    draw_rasgulla(
        screen,
        center_x,
        int(y),
        190
    )

    # Syrup drops
    for drop in syrup_drops:

        drop[1] += drop[2]

        if drop[1] > HEIGHT:
            drop[1] = random.randint(450, 500)
            drop[0] = random.randint(200, 800)

        pygame.draw.circle(
            screen,
            GOLD,
            (int(drop[0]), int(drop[1])),
            drop[3]
        )

    # Title
    title = font.render(
        "THE GIANT RASGULLA",
        True,
        GOLD
    )

    screen.blit(
        title,
        (WIDTH//2-title.get_width()//2, 35)
    )

    subtitle = small.render(
        "Soft • Spongy • Sweet • Delicious",
        True,
        WHITE
    )

    screen.blit(
        subtitle,
        (WIDTH//2-subtitle.get_width()//2, 85)
    )

    instruction = small.render(
        "SPACE = Restart    ESC = Exit",
        True,
        WHITE
    )

    screen.blit(
        instruction,
        (WIDTH//2-instruction.get_width()//2, 700)
    )

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
