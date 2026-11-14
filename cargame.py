
import pygame
import random
import sys
import math

# ---------------- INITIALIZATION ----------------
pygame.init()

WIDTH, HEIGHT = 900, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("NEON RACER - Car Racing Game")

clock = pygame.time.Clock()

# Colors
BLACK = (10, 12, 20)
WHITE = (255, 255, 255)
GREEN = (25, 110, 55)
DARK_GREEN = (15, 75, 40)
ROAD = (42, 43, 50)
ROAD_LINE = (230, 230, 230)
RED = (245, 50, 65)
BLUE = (40, 150, 255)
YELLOW = (255, 210, 50)

# Fonts
font = pygame.font.SysFont("Arial", 25, bold=True)
big_font = pygame.font.SysFont("Arial", 55, bold=True)
small_font = pygame.font.SysFont("Arial", 18)

# Road dimensions
ROAD_LEFT = 190
ROAD_RIGHT = 710
ROAD_WIDTH = ROAD_RIGHT - ROAD_LEFT

LANES = [
    ROAD_LEFT + ROAD_WIDTH // 6,
    ROAD_LEFT + ROAD_WIDTH // 2,
    ROAD_LEFT + ROAD_WIDTH * 5 // 6
]

# ---------------- GAME VARIABLES ----------------
player_x = WIDTH // 2
player_y = HEIGHT - 125

PLAYER_WIDTH = 52
PLAYER_HEIGHT = 95

player_speed = 420

enemy_cars = []

score = 0
high_score = 0

game_speed = 350
spawn_timer = 0
road_offset = 0
game_time = 0

game_over = False
paused = False
started = False

# ---------------- DRAW CAR ----------------
def draw_car(surface, x, y, color, player=False):

    x = int(x)
    y = int(y)

    width = PLAYER_WIDTH
    height = PLAYER_HEIGHT

    # Wheels
    pygame.draw.rect(
        surface, BLACK,
        (x - 6, y + 17, 9, 24),
        border_radius=4
    )

    pygame.draw.rect(
        surface, BLACK,
        (x + width - 3, y + 17, 9, 24),
        border_radius=4
    )

    pygame.draw.rect(
        surface, BLACK,
        (x - 6, y + 58, 9, 24),
        border_radius=4
    )

    pygame.draw.rect(
        surface, BLACK,
        (x + width - 3, y + 58, 9, 24),
        border_radius=4
    )

    # Main body
    pygame.draw.rect(
        surface, color,
        (x, y, width, height),
        border_radius=13
    )

    # Front windshield
    pygame.draw.polygon(
        surface,
        (100, 190, 230),
        [
            (x + 9, y + 19),
            (x + width - 9, y + 19),
            (x + width - 13, y + 43),
            (x + 13, y + 43)
        ]
    )

    # Rear windshield
    pygame.draw.polygon(
        surface,
        (50, 100, 145),
        [
            (x + 13, y + 56),
            (x + width - 13, y + 56),
            (x + width - 10, y + 76),
            (x + 10, y + 76)
        ]
    )

    # Side mirrors
    pygame.draw.rect(
        surface, color,
        (x - 5, y + 32, 7, 13),
        border_radius=3
    )

    pygame.draw.rect(
        surface, color,
        (x + width - 2, y + 32, 7, 13),
        border_radius=3
    )

    # Headlights
    if player:
        pygame.draw.rect(
            surface, YELLOW,
            (x + 5, y + 5, 11, 7),
            border_radius=3
        )

        pygame.draw.rect(
            surface, YELLOW,
            (x + width - 16, y + 5, 11, 7),
            border_radius=3
        )

        # Racing stripe
        pygame.draw.rect(
            surface, WHITE,
            (x + 23, y + 5, 6, 85)
        )

    else:
        pygame.draw.rect(
            surface, RED,
            (x + 5, y + height - 10, 12, 6),
            border_radius=2
        )

        pygame.draw.rect(
            surface, RED,
            (x + width - 17, y + height - 10, 12, 6),
            border_radius=2
        )


# ---------------- BACKGROUND ----------------
def draw_background():

    screen.fill(DARK_GREEN)

    # Grass texture
    for i in range(0, HEIGHT, 80):
        pygame.draw.rect(
            screen,
            GREEN,
            (0, i, ROAD_LEFT - 12, 40)
        )

        pygame.draw.rect(
            screen,
            GREEN,
            (ROAD_RIGHT + 12, i, WIDTH - ROAD_RIGHT, 40)
        )

    # Road
    pygame.draw.rect(
        screen,
        ROAD,
        (ROAD_LEFT, 0, ROAD_WIDTH, HEIGHT)
    )

    # Road borders
    pygame.draw.rect(
        screen, WHITE,
        (ROAD_LEFT - 6, 0, 6, HEIGHT)
    )

    pygame.draw.rect(
        screen, WHITE,
        (ROAD_RIGHT, 0, 6, HEIGHT)
    )

    # Moving lane markings
    for lane_x in [
        ROAD_LEFT + ROAD_WIDTH // 3,
        ROAD_LEFT + ROAD_WIDTH * 2 // 3
    ]:

        for y in range(-100, HEIGHT, 100):

            pygame.draw.rect(
                screen,
                ROAD_LINE,
                (lane_x - 3, y + road_offset, 6, 55)
            )

    # Side trees
    for y in range(-100, HEIGHT, 140):

        pos = (y + int(road_offset)) % (HEIGHT + 100) - 50

        for x in [90, 810]:

            pygame.draw.circle(
                screen, (10, 55, 25),
                (x, pos + 5), 24
            )

            pygame.draw.circle(
                screen, (30, 145, 65),
                (x, pos), 20
            )

            pygame.draw.rect(
                screen, (110, 65, 30),
                (x - 4, pos + 13, 8, 17)
            )


# ---------------- SPAWN ENEMY ----------------
def spawn_enemy():

    lane = random.choice(LANES)

    colors = [
        RED,
        BLUE,
        YELLOW,
        (180, 70, 220),
        (240, 240, 240),
        (255, 120, 35)
    ]

    enemy_cars.append({
        "x": lane - PLAYER_WIDTH // 2,
        "y": -120,
        "speed": random.randint(20, 100),
        "color": random.choice(colors)
    })


# ---------------- DRAW HUD ----------------
def draw_hud():

    pygame.draw.rect(
        screen, (10, 15, 30),
        (15, 15, 210, 100),
        border_radius=12
    )

    score_text = font.render(
        f"SCORE: {int(score)}", True, WHITE
    )

    speed_text = small_font.render(
        f"SPEED: {int(game_speed / 10)} KM/H",
        True, YELLOW
    )

    high_text = small_font.render(
        f"BEST: {high_score}", True, WHITE
    )

    screen.blit(score_text, (30, 25))
    screen.blit(speed_text, (30, 62))
    screen.blit(high_text, (30, 85))


# ---------------- RESET GAME ----------------
def reset_game():

    global player_x, enemy_cars
    global score, game_speed
    global spawn_timer, road_offset
    global game_time, game_over, paused

    player_x = WIDTH // 2 - PLAYER_WIDTH // 2

    enemy_cars = []

    score = 0
    game_speed = 350
    spawn_timer = 0
    road_offset = 0
    game_time = 0

    game_over = False
    paused = False


# ---------------- GAME OVER SCREEN ----------------
def draw_game_over():

    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 185))

    screen.blit(overlay, (0, 0))

    title = big_font.render("GAME OVER", True, RED)

    score_text = font.render(
        f"YOUR SCORE: {int(score)}", True, WHITE
    )

    best_text = font.render(
        f"BEST SCORE: {high_score}", True, YELLOW
    )

    restart_text = font.render(
        "PRESS R TO RESTART", True, WHITE
    )

    exit_text = small_font.render(
        "PRESS ESC TO EXIT", True, WHITE
    )

    screen.blit(
        title,
        title.get_rect(center=(WIDTH // 2, 260))
    )

    screen.blit(
        score_text,
        score_text.get_rect(center=(WIDTH // 2, 345))
    )

    screen.blit(
        best_text,
        best_text.get_rect(center=(WIDTH // 2, 395))
    )

    screen.blit(
        restart_text,
        restart_text.get_rect(center=(WIDTH // 2, 475))
    )

    screen.blit(
        exit_text,
        exit_text.get_rect(center=(WIDTH // 2, 520))
    )


# ---------------- START SCREEN ----------------
def draw_start_screen():

    screen.fill((8, 12, 28))

    title = big_font.render("NEON RACER", True, YELLOW)

    subtitle = font.render(
        "ULTIMATE CAR RACING GAME", True, WHITE
    )

    start = font.render(
        "PRESS ENTER TO START", True, (50, 255, 130)
    )

    controls = small_font.render(
        "ARROW KEYS / A-D TO DRIVE", True, WHITE
    )

    screen.blit(
        title,
        title.get_rect(center=(WIDTH // 2, 250))
    )

    screen.blit(
        subtitle,
        subtitle.get_rect(center=(WIDTH // 2, 320))
    )

    screen.blit(
        start,
        start.get_rect(center=(WIDTH // 2, 420))
    )

    screen.blit(
        controls,
        controls.get_rect(center=(WIDTH // 2, 475))
    )


# ---------------- MAIN GAME LOOP ----------------
running = True

while running:

    dt = clock.tick(60) / 1000

    # ---------------- EVENTS ----------------
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                running = False

            if not started and event.key == pygame.K_RETURN:
                started = True
                reset_game()

            elif game_over and event.key == pygame.K_r:
                reset_game()

            elif started and not game_over:
                if event.key == pygame.K_p:
                    paused = not paused

    if not started:

        draw_start_screen()

    elif not game_over:

        if not paused:

            keys = pygame.key.get_pressed()

            # Player movement
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                player_x -= player_speed * dt

            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                player_x += player_speed * dt

            # Keep player inside road
            player_x = max(
                ROAD_LEFT + 8,
                min(
                    ROAD_RIGHT - PLAYER_WIDTH - 8,
                    player_x
                )
            )

            # Difficulty increase
            game_time += dt

            game_speed = min(
                850,
                350 + game_time * 12
            )

            score += dt * (game_speed / 30)

            # Road animation
            road_offset += game_speed * dt
            road_offset %= 100

            # Enemy spawning
            spawn_timer += dt

            spawn_interval = max(
                0.55,
                1.3 - game_time * 0.008
            )

            if spawn_timer >= spawn_interval:
                spawn_enemy()
                spawn_timer = 0

            # Move enemies
            for enemy in enemy_cars:
                enemy["y"] += (
                    game_speed + enemy["speed"]
                ) * dt

            # Remove enemies outside screen
            enemy_cars = [
                enemy for enemy in enemy_cars
                if enemy["y"] < HEIGHT + 150
            ]

            # Collision detection
            player_rect = pygame.Rect(
                int(player_x) + 5,
                player_y + 8,
                PLAYER_WIDTH - 10,
                PLAYER_HEIGHT - 16
            )

            for enemy in enemy_cars:

                enemy_rect = pygame.Rect(
                    int(enemy["x"]) + 5,
                    int(enemy["y"]) + 8,
                    PLAYER_WIDTH - 10,
                    PLAYER_HEIGHT - 16
                )

                if player_rect.colliderect(enemy_rect):
                    game_over = True

            high_score = max(high_score, int(score))

        # ---------------- DRAW GAME ----------------
        draw_background()

        # Player
        draw_car(
            screen,
            player_x,
            player_y,
            BLUE,
            player=True
        )

        # Enemy cars
        for enemy in enemy_cars:

            draw_car(
                screen,
                enemy["x"],
                enemy["y"],
                enemy["color"]
            )

        draw_hud()

        # Pause screen
        if paused:

            pause_text = big_font.render(
                "PAUSED", True, YELLOW
            )

            screen.blit(
                pause_text,
                pause_text.get_rect(
                    center=(WIDTH // 2, HEIGHT // 2)
                )
            )

        if game_over:
            draw_game_over()

    else:

        draw_background()
        draw_game_over()

    pygame.display.flip()


pygame.quit()
sys.exit()
