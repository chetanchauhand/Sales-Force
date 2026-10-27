
import pygame
import random
import math

pygame.init()

WIDTH, HEIGHT = 1000, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🏸 Badminton Game")

clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 24, bold=True)
big_font = pygame.font.SysFont("arial", 42, bold=True)

# Colors
WHITE = (255, 255, 255)
GREEN = (20, 150, 95)
DARK_GREEN = (10, 100, 65)
BLUE = (40, 130, 255)
RED = (245, 65, 75)
BLACK = (25, 30, 40)
YELLOW = (255, 225, 90)

# Court and net
NET_X = WIDTH // 2
COURT_TOP = 250
COURT_BOTTOM = 560

# Players
p1 = pygame.Vector2(200, 470)
p2 = pygame.Vector2(800, 470)
PLAYER_SPEED = 5

score1 = 0
score2 = 0

# Shuttlecock physics
shuttle = pygame.Vector2(350, 320)
velocity = pygame.Vector2(4, -3)
gravity = 0.12
last_hitter = 1
game_over = False
winner = ""

def draw_text(text, x, y, color=WHITE, font_obj=font):
    img = font_obj.render(text, True, color)
    screen.blit(img, (x, y))

def draw_court():
    screen.fill((18, 30, 65))

    # Stadium lights
    for x in range(70, WIDTH, 140):
        pygame.draw.circle(screen, YELLOW, (x, 90), 4)
        pygame.draw.circle(screen, (80, 100, 150), (x, 90), 12, 1)

    # Court floor
    pygame.draw.rect(
        screen, GREEN,
        (40, COURT_TOP, WIDTH - 80, COURT_BOTTOM - COURT_TOP)
    )

    # Court boundary lines
    pygame.draw.rect(
        screen, WHITE,
        (40, COURT_TOP, WIDTH - 80, COURT_BOTTOM - COURT_TOP), 3
    )

    pygame.draw.line(
        screen, WHITE, (NET_X, COURT_TOP),
        (NET_X, COURT_BOTTOM), 3
    )

    pygame.draw.line(
        screen, WHITE, (40, 400),
        (WIDTH - 40, 400), 2
    )

    pygame.draw.line(
        screen, WHITE, (250, COURT_TOP),
        (250, COURT_BOTTOM), 2
    )

    pygame.draw.line(
        screen, WHITE, (750, COURT_TOP),
        (750, COURT_BOTTOM), 2
    )

    # Net
    pygame.draw.line(
        screen, WHITE, (NET_X, 290), (NET_X, 510), 5
    )

    for y in range(295, 510, 12):
        pygame.draw.line(
            screen, (180, 205, 220),
            (NET_X - 12, y), (NET_X + 12, y), 1
        )

    pygame.draw.rect(
        screen, BLACK, (0, 570, WIDTH, 80)
    )

def draw_player(pos, color, facing):
    x, y = int(pos.x), int(pos.y)

    # Shadow
    pygame.draw.ellipse(
        screen, DARK_GREEN, (x - 25, y + 25, 50, 12)
    )

    # Legs
    pygame.draw.line(
        screen, BLACK, (x - 8, y + 12),
        (x - 15, y + 28), 7
    )
    pygame.draw.line(
        screen, BLACK, (x + 8, y + 12),
        (x + 16, y + 28), 7
    )

    # Body
    pygame.draw.ellipse(
        screen, color, (x - 17, y - 18, 34, 43)
    )

    # Head
    pygame.draw.circle(
        screen, (255, 205, 160), (x, y - 30), 13
    )

    # Hair
    pygame.draw.arc(
        screen, BLACK,
        (x - 13, y - 43, 26, 23), 0, math.pi, 5
    )

    # Eyes
    pygame.draw.circle(
        screen, BLACK,
        (x + facing * 5, y - 31), 2
    )

    # Racket arm
    racket_x = x + facing * 25
    racket_y = y - 5

    pygame.draw.line(
        screen, (255, 205, 160),
        (x + facing * 10, y - 8),
        (racket_x, racket_y), 5
    )

    # Racket handle
    pygame.draw.line(
        screen, BLACK,
        (racket_x, racket_y),
        (racket_x + facing * 18, racket_y - 18), 4
    )

    # Racket head
    racket_center = (
        racket_x + facing * 25, racket_y - 30
    )

    pygame.draw.ellipse(
        screen, WHITE,
        (racket_center[0] - 11, racket_center[1] - 16,
         22, 32), 2
    )

    pygame.draw.line(
        screen, WHITE,
        (racket_center[0] - 8, racket_center[1] - 10),
        (racket_center[0] + 8, racket_center[1] + 10), 1
    )

    pygame.draw.line(
        screen, WHITE,
        (racket_center[0] + 8, racket_center[1] - 10),
        (racket_center[0] - 8, racket_center[1] + 10), 1
    )

def draw_shuttle():
    x, y = int(shuttle.x), int(shuttle.y)

    # Feather cone
    points = [
        (x, y),
        (x - 12, y - 7),
        (x - 9, y + 8),
        (x + 3, y + 10)
    ]

    pygame.draw.polygon(screen, WHITE, points)
    pygame.draw.circle(screen, YELLOW, (x, y), 4)

    # Motion trail
    pygame.draw.line(
        screen, (200, 220, 255),
        (x - velocity.x * 3, y - velocity.y * 3),
        (x - velocity.x * 6, y - velocity.y * 6), 2
    )

def reset_shuttle(direction):
    global shuttle, velocity, last_hitter

    shuttle = pygame.Vector2(NET_X, 330)

    velocity = pygame.Vector2(
        random.choice([4, 5, 6]) * direction,
        random.choice([-5, -4, -3])
    )

    last_hitter = 1 if direction > 0 else 2

def hit_shuttle(player, player_number):
    global velocity, last_hitter

    distance = player.distance_to(shuttle)

    if distance < 100 and shuttle.y > 190:
        direction = 1 if player_number == 1 else -1

        velocity.x = direction * random.uniform(5, 8)
        velocity.y = random.uniform(-7, -4)

        last_hitter = player_number
        return True

    return False

def keep_player_in_court(player, left, right):
    player.x = max(left, min(right, player.x))
    player.y = max(410, min(535, player.y))

running = True

reset_shuttle(random.choice([-1, 1]))

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            if game_over and event.key == pygame.K_r:
                score1 = 0
                score2 = 0
                game_over = False
                winner = ""
                reset_shuttle(random.choice([-1, 1]))

            if not game_over:
                if event.key == pygame.K_SPACE:
                    hit_shuttle(p1, 1)

                if event.key == pygame.K_SLASH:
                    hit_shuttle(p2, 2)

    keys = pygame.key.get_pressed()

    if not game_over:
        # Player 1: WASD
        if keys[pygame.K_a]:
            p1.x -= PLAYER_SPEED
        if keys[pygame.K_d]:
            p1.x += PLAYER_SPEED
        if keys[pygame.K_w]:
            p1.y -= PLAYER_SPEED
        if keys[pygame.K_s]:
            p1.y += PLAYER_SPEED

        # Player 2: Arrow keys
        if keys[pygame.K_LEFT]:
            p2.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            p2.x += PLAYER_SPEED
        if keys[pygame.K_UP]:
            p2.y -= PLAYER_SPEED
        if keys[pygame.K_DOWN]:
            p2.y += PLAYER_SPEED

        keep_player_in_court(p1, 65, NET_X - 45)
        keep_player_in_court(p2, NET_X + 45, WIDTH - 65)

        # Shuttlecock movement
        shuttle.x += velocity.x
        shuttle.y += velocity.y
        velocity.y += gravity

        # Ground / net collision
        if shuttle.y >= COURT_BOTTOM - 5:
            if shuttle.x < NET_X:
                score2 += 1
            else:
                score1 += 1

            if score1 >= 11 or score2 >= 11:
                game_over = True
                winner = "Player 1" if score1 > score2 else "Player 2"
            else:
                reset_shuttle(random.choice([-1, 1]))

        # Net collision
        if abs(shuttle.x - NET_X) < 10 and 290 < shuttle.y < 510:
            velocity.x *= -0.8
            shuttle.x += velocity.x * 2

        # Out of bounds
        if shuttle.x < 40 or shuttle.x > WIDTH - 40:
            if last_hitter == 1:
                score2 += 1
            else:
                score1 += 1

            if score1 >= 11 or score2 >= 11:
                game_over = True
                winner = "Player 1" if score1 > score2 else "Player 2"
            else:
                reset_shuttle(random.choice([-1, 1]))

    # Draw everything
    draw_court()

    draw_player(p1, BLUE, 1)
    draw_player(p2, RED, -1)
    draw_shuttle()

    draw_text("PLAYER 1", 90, 35, BLUE)
    draw_text(str(score1), 135, 70, WHITE, big_font)

    draw_text("PLAYER 2", 790, 35, RED)
    draw_text(str(score2), 835, 70, WHITE, big_font)

    draw_text("BADMINTON CHAMPIONSHIP", 315, 15, YELLOW)

    if game_over:
        pygame.draw.rect(
            screen, BLACK, (240, 235, 520, 180),
            border_radius=20
        )

        draw_text(
            winner + " WINS!",
            350, 265, YELLOW, big_font
        )

        draw_text(
            "Press R to Play Again",
            355, 325, WHITE
        )

    else:
        draw_text(
            "P1: WASD + SPACE",
            45, 600, WHITE
        )

        draw_text(
            "P2: ARROWS + /",
            650, 600, WHITE
        )

    pygame.display.flip()

pygame.quit()
