
import pygame
import math
import sys

pygame.init()

WIDTH, HEIGHT = 900, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Live Jalebi Animation")

clock = pygame.time.Clock()

# Colors
BG = (25, 15, 12)
GOLD = (255, 155, 15)
ORANGE = (255, 95, 5)
YELLOW = (255, 205, 55)
WHITE = (255, 240, 180)

font = pygame.font.SysFont("Arial", 28, bold=True)
small_font = pygame.font.SysFont("Arial", 18)

center_x, center_y = WIDTH // 2, HEIGHT // 2

angle = 0
draw_progress = 0
rotation = 0

def jalebi_points(progress, rotation):
    points = []

    total = 2200

    for i in range(int(total * progress)):
        t = i / total

        # Spiral structure
        theta = t * math.pi * 18 + rotation
        radius = 15 + t * 180

        # Spiral with circular loops
        x = radius * math.cos(theta)
        y = radius * math.sin(theta)

        # Add extra circular curves
        x += 28 * math.cos(theta * 3)
        y += 28 * math.sin(theta * 3)

        points.append((center_x + x, center_y + y))

    return points


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
                draw_progress = 0

    # Background decorative circles
    for i in range(8):
        pygame.draw.circle(
            screen,
            (45, 25, 15),
            (center_x, center_y),
            220 + i * 15,
            1
        )

    # Animation
    if draw_progress < 1:
        draw_progress += 0.003

    rotation += 0.002

    points = jalebi_points(draw_progress, rotation)

    if len(points) > 2:

        # Outer syrup shadow
        pygame.draw.lines(
            screen,
            (130, 48, 5),
            False,
            points,
            23
        )

        # Orange jalebi body
        pygame.draw.lines(
            screen,
            ORANGE,
            False,
            points,
            17
        )

        # Golden highlights
        pygame.draw.lines(
            screen,
            YELLOW,
            False,
            points,
            5
        )

    # Title
    title = font.render("HOT & CRISPY JALEBI", True, GOLD)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 40))

    subtitle = small_font.render(
        "Freshly made with love!",
        True,
        WHITE
    )
    screen.blit(
        subtitle,
        (WIDTH // 2 - subtitle.get_width() // 2, 82)
    )

    # Instructions
    instruction = small_font.render(
        "SPACE = Restart Animation    ESC = Exit",
        True,
        WHITE
    )
    screen.blit(
        instruction,
        (WIDTH // 2 - instruction.get_width() // 2, 650)
    )

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
