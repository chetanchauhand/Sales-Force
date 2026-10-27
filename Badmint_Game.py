
import pygame
import random
import math

pygame.init()

# ---------------- SETTINGS ----------------
WIDTH, HEIGHT = 1000, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Badminton Championship - VS Computer")
clock = pygame.time.Clock()

WHITE = (245, 250, 255)
BLACK = (15, 22, 38)
GREEN = (20, 145, 90)
BLUE = (45, 140, 255)
RED = (245, 65, 85)
YELLOW = (255, 220, 85)
CYAN = (80, 225, 255)
GREY = (160, 180, 205)

font = pygame.font.SysFont("arial", 23, bold=True)
small_font = pygame.font.SysFont("arial", 17)
title_font = pygame.font.SysFont("arial", 44, bold=True)
score_font = pygame.font.SysFont("arial", 38, bold=True)

NET_X = WIDTH // 2
FLOOR_Y = 535
COURT_LEFT = 40
COURT_RIGHT = WIDTH - 40

# Mode settings: AI speed, reaction time, hit reach
MODES = {
    "EASY":   {"speed": 3.0, "reaction": 450, "reach": 78},
    "MEDIUM": {"speed": 4.0, "reaction": 220, "reach": 95},
    "HARD":   {"speed": 5.2, "reaction": 90,  "reach": 115},
}

mode = None
level = 1
player_score = 0
computer_score = 0

player = pygame.Vector2(180, 440)
computer = pygame.Vector2(820, 440)
shuttle = pygame.Vector2(NET_X, 350)
velocity = pygame.Vector2(4, -4)

player_hit_time = 0
computer_hit_time = 0
last_hitter = 0

state = "menu"
message = ""
message_until = 0
serve_time = 0


# ---------------- HELPERS ----------------
def draw_text(text, x, y, color=WHITE, f=font, center=False):
    image = f.render(str(text), True, color)

    if center:
        screen.blit(image, (x - image.get_width() // 2, y))
    else:
        screen.blit(image, (x, y))


def reset_round():
    global shuttle, velocity, serve_time
    global player_hit_time, computer_hit_time, last_hitter

    player.update(180, 440)
    computer.update(820, 440)
    shuttle.update(NET_X, 345)

    # Alternate serving direction
    direction = random.choice([-1, 1])
    velocity.update(direction * 4, -4)

    player_hit_time = 0
    computer_hit_time = 0
    last_hitter = 0
    serve_time = pygame.time.get_ticks()


def start_match(selected_mode):
    global mode, level, player_score, computer_score, state, message

    mode = selected_mode
    level = 1
    player_score = 0
    computer_score = 0
    message = ""
    state = "playing"
    reset_round()


def draw_court():
    screen.fill((13, 24, 53))

    # Stadium lights
    for x in range(75, WIDTH, 140):
        pygame.draw.circle(screen, CYAN, (x, 95), 5)
        pygame.draw.circle(screen, (50, 95, 155), (x, 95), 14, 1)

    # Background stands
    for row in range(3):
        for x in range(20, WIDTH, 45):
            y = 160 + row * 38
            pygame.draw.circle(
                screen,
                random_color(row, x),
                (x, y), 7
            )

    # Court
    pygame.draw.rect(
        screen, GREEN,
        (COURT_LEFT, 260, WIDTH - 80, FLOOR_Y - 260)
    )

    pygame.draw.rect(
        screen, WHITE,
        (COURT_LEFT, 260, WIDTH - 80, FLOOR_Y - 260), 3
    )

    # Service lines
    pygame.draw.line(
        screen, WHITE, (COURT_LEFT, 390),
        (COURT_RIGHT, 390), 2
    )

    pygame.draw.line(
        screen, WHITE, (250, 260), (250, FLOOR_Y), 2
    )

    pygame.draw.line(
        screen, WHITE, (750, 260), (750, FLOOR_Y), 2
    )

    # Center net
    pygame.draw.line(
        screen, WHITE, (NET_X, 285), (NET_X, 510), 5
    )

    for y in range(290, 510, 12):
        pygame.draw.line(
            screen, GREY,
            (NET_X - 13, y), (NET_X + 13, y), 1
        )

    # Floor
    pygame.draw.rect(screen, BLACK, (0, 570, WIDTH, 80))


def random_color(row, x):
    colors = [
        (40, 65, 105),
        (55, 80, 125),
        (45, 55, 95)
    ]
    return colors[(row + x // 45) % len(colors)]


def draw_player(pos, color, facing, is_computer=False):
    x, y = int(pos.x), int(pos.y)

    # Shadow
    pygame.draw.ellipse(
        screen, (10, 80, 55), (x - 24, y + 23, 48, 12)
    )

    # Legs
    pygame.draw.line(
        screen, BLACK, (x - 8, y + 10),
        (x - 15, y + 28), 7
    )
    pygame.draw.line(
        screen, BLACK, (x + 8, y + 10),
        (x + 15, y + 28), 7
    )

    # Body
    pygame.draw.ellipse(
        screen, color, (x - 17, y - 20, 34, 42)
    )

    # Head
    pygame.draw.circle(
        screen, (255, 204, 160), (x, y - 31), 13
    )

    # Hair
    pygame.draw.arc(
        screen, BLACK,
        (x - 13, y - 44, 26, 22), 0, math.pi, 5
    )

    # Eyes
    pygame.draw.circle(
        screen, BLACK, (x + facing * 5, y - 32), 2
    )

    # Racket
    arm = (x + facing * 15, y - 9)
    racket = (x + facing * 32, y - 26)

    pygame.draw.line(
        screen, (255, 204, 160), arm, racket, 5
    )

    pygame.draw.line(
        screen, BLACK, racket,
        (racket[0] + facing * 12, racket[1] - 14), 4
    )

    pygame.draw.ellipse(
        screen, WHITE,
        (racket[0] + facing * 12 - 10,
         racket[1] - 34, 20, 30), 2
    )

    pygame.draw.line(
        screen, CYAN,
        (racket[0] + facing * 12 - 7, racket[1] - 28),
        (racket[0] + facing * 12 + 7, racket[1] - 10), 1
    )


def draw_shuttle():
    x, y = int(shuttle.x), int(shuttle.y)

    # Motion trail
    for i in range(1, 5):
        tx = int(x - velocity.x * i * 2)
        ty = int(y - velocity.y * i * 2)
        pygame.draw.circle(
            screen, (100, 155, 190),
            (tx, ty), max(1, 4 - i)
        )

    # Shuttle feathers and cork
    pygame.draw.polygon(
        screen, WHITE,
        [(x, y), (x - 12, y - 8),
         (x - 10, y + 7), (x + 3, y + 9)]
    )
    pygame.draw.circle(screen, YELLOW, (x, y), 4)


def hit_shuttle(is_player):
    global velocity, last_hitter
    global player_hit_time, computer_hit_time

    now = pygame.time.get_ticks()

    if is_player:
        if now - player_hit_time < 300:
            return

        # Player can only hit shuttle on their own side
        if shuttle.x >= NET_X - 8:
            return

        if player.distance_to(shuttle) > 100:
            return

        player_hit_time = now
        direction = 1

    else:
        if now - computer_hit_time < 350:
            return

        if shuttle.x <= NET_X + 8:
            return

        if computer.distance_to(shuttle) > MODES[mode]["reach"]:
            return

        computer_hit_time = now
        direction = -1

    # Hit sends shuttle towards opponent
    velocity.x = direction * random.uniform(5.5, 7.5)

    # Aim based on racket contact and level
    if is_player:
        aim = (shuttle.y - player.y) / 12
    else:
        aim = (shuttle.y - computer.y) / 12

    velocity.y = max(-8.5, min(-3.0, aim - 4))

    last_hitter = 1 if is_player else 2


def award_point(winner):
    global player_score, computer_score, state
    global message, message_until, level

    if winner == "player":
        player_score += 1
        message = "NICE SHOT! +1 POINT"
    else:
        computer_score += 1
        message = "COMPUTER SCORES!"

    message_until = pygame.time.get_ticks() + 900

    if player_score >= 11 or computer_score >= 11:
        if player_score > computer_score:
            state = "level_won"
        else:
            state = "lost"

        return

    reset_round()


def move_towards(pos, target_x, target_y, speed):
    dx = target_x - pos.x
    dy = target_y - pos.y
    distance = math.hypot(dx, dy)

    if distance > speed and distance != 0:
        pos.x += dx / distance * speed
        pos.y += dy / distance * speed
    elif distance > 0:
        pos.update(target_x, target_y)


# ---------------- MAIN LOOP ----------------
running = True

while running:
    clock.tick(60)
    now = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            if state == "menu":
                if event.key == pygame.K_1:
                    start_match("EASY")
                elif event.key == pygame.K_2:
                    start_match("MEDIUM")
                elif event.key == pygame.K_3:
                    start_match("HARD")

            elif state == "playing":
                if event.key == pygame.K_SPACE:
                    hit_shuttle(True)

            elif state in ("lost", "level_won"):
                if event.key == pygame.K_r:
                    if state == "level_won":
                        level += 1

                    player_score = 0
                    computer_score = 0
                    state = "playing"
                    reset_round()

                elif event.key == pygame.K_m:
                    state = "menu"

    keys = pygame.key.get_pressed()

    if state == "playing":
        # -------- PLAYER MOVEMENT --------
        speed = 5

        if keys[pygame.K_LEFT]:
            player.x -= speed
        if keys[pygame.K_RIGHT]:
            player.x += speed
        if keys[pygame.K_UP]:
            player.y -= speed
        if keys[pygame.K_DOWN]:
            player.y += speed

        player.x = max(65, min(NET_X - 45, player.x))
        player.y = max(330, min(FLOOR_Y - 15, player.y))

        # Space works even when held down
        if keys[pygame.K_SPACE]:
            hit_shuttle(True)

        # -------- COMPUTER AI --------
        settings = MODES[mode]

        # Higher levels improve AI speed and reach
        ai_speed = min(
            settings["speed"] + (level - 1) * 0.35,
            7.0
        )

        ai_reach = min(
            settings["reach"] + (level - 1) * 3,
            150
        )

        # Computer predicts where shuttle will travel
        target_x = 820
        target_y = 440

        if shuttle.x > NET_X:
            if velocity.x > 0:
                frames = max(
                    0, (computer.x - shuttle.x) /
                    max(abs(velocity.x), 1)
                )

                target_x = shuttle.x + velocity.x * min(frames, 10)
                target_y = shuttle.y + velocity.y * 4

            else:
                target_x = max(650, shuttle.x + 90)
                target_y = shuttle.y

        # Easy mode has slower reaction
        reaction_delay = max(
            35, settings["reaction"] - (level - 1) * 15
        )

        if now - computer_hit_time > reaction_delay:
            move_towards(
                computer,
                max(NET_X + 45, min(935, target_x)),
                max(330, min(FLOOR_Y - 15, target_y)),
                ai_speed
            )

        # Keep computer on its side
        computer.x = max(NET_X + 45, min(935, computer.x))
        computer.y = max(330, min(FLOOR_Y - 15, computer.y))

        # AI automatically returns nearby shuttlecock
        if (
            shuttle.x > NET_X + 8
            and computer.distance_to(shuttle) < ai_reach
            and velocity.x > 0
            and now - computer_hit_time > reaction_delay
        ):
            hit_shuttle(False)

        # -------- SHUTTLE PHYSICS --------
        shuttle.x += velocity.x
        shuttle.y += velocity.y
        velocity.y += 0.13

        # Net collision
        if (
            abs(shuttle.x - NET_X) < 10
            and shuttle.y > 285
            and abs(shuttle.y - 285) > 0
        ):
            # Only block shuttle if it crosses the net too low
            if shuttle.y > 305:
                if last_hitter == 1:
                    award_point("computer")
                elif last_hitter == 2:
                    award_point("player")
                else:
                    award_point(
                        "computer" if shuttle.x < NET_X else "player"
                    )

        # Ground collision
        if state == "playing" and shuttle.y >= FLOOR_Y:
            if shuttle.x < NET_X:
                award_point("computer")
            else:
                award_point("player")

        # Out of court
        if state == "playing" and (
            shuttle.x < COURT_LEFT or shuttle.x > COURT_RIGHT
        ):
            if last_hitter == 1:
                award_point("computer")
            else:
                award_point("player")

    # -------- RENDER --------
    draw_court()

    # Header
    pygame.draw.rect(
        screen, (18, 40, 82), (15, 12, 300, 95),
        border_radius=15
    )
    pygame.draw.rect(
        screen, (85, 30, 60), (685, 12, 300, 95),
        border_radius=15
    )

    draw_text("YOU", 50, 22, CYAN)
    draw_text(str(player_score), 50, 52, WHITE, score_font)

    draw_text("COMPUTER", 720, 22, RED)
    draw_text(str(computer_score), 720, 52, WHITE, score_font)

    draw_text(
        "BADMINTON CHAMPIONSHIP",
        WIDTH // 2, 18, YELLOW, font, center=True
    )

    if mode:
        draw_text(
            f"MODE: {mode}    LEVEL: {level}",
            WIDTH // 2, 55, WHITE, small_font, center=True
        )

    draw_player(player, BLUE, 1)
    draw_player(computer, RED, -1, True)
    draw_shuttle()

    if state == "playing":
        draw_text(
            "ARROWS: MOVE     SPACE: HIT",
            WIDTH // 2, 600, WHITE, small_font, center=True
        )

        if now < message_until:
            draw_text(
                message, WIDTH // 2, 215,
                YELLOW, font, center=True
            )

    # -------- MENU --------
    if state == "menu":
        pygame.draw.rect(
            screen, BLACK, (230, 180, 540, 310),
            border_radius=25
        )

        draw_text(
            "BADMINTON VS COMPUTER",
            WIDTH // 2, 205, CYAN, title_font, center=True
        )

        draw_text(
            "SELECT DIFFICULTY",
            WIDTH // 2, 275, WHITE, font, center=True
        )

        draw_text(
            "1  -  EASY",
            WIDTH // 2, 325, (90, 230, 130), font, center=True
        )

        draw_text(
            "2  -  MEDIUM",
            WIDTH // 2, 365, YELLOW, font, center=True
        )

        draw_text(
            "3  -  HARD",
            WIDTH // 2, 405, RED, font, center=True
        )

        draw_text(
            "Use arrow keys to move and SPACE to hit",
            WIDTH // 2, 455, WHITE, small_font, center=True
        )

    # -------- WIN / LOSE --------
    if state in ("level_won", "lost"):
        pygame.draw.rect(
            screen, BLACK, (210, 205, 580, 250),
            border_radius=25
        )

        if state == "level_won":
            draw_text(
                "YOU WIN!",
                WIDTH // 2, 230, YELLOW, title_font, center=True
            )

            draw_text(
                f"LEVEL {level} COMPLETED",
                WIDTH // 2, 295, CYAN, font, center=True
            )

            draw_text(
                "Press R for the next, harder level",
                WIDTH // 2, 350, WHITE, small_font, center=True
            )

        else:
            draw_text(
                "COMPUTER WINS!",
                WIDTH // 2, 235, RED, title_font, center=True
            )

            draw_text(
                f"Final Score: {player_score} - {computer_score}",
                WIDTH // 2, 305, WHITE, font, center=True
            )

            draw_text(
                "Press R to retry this level",
                WIDTH // 2, 355, CYAN, small_font, center=True
            )

        draw_text(
            "Press M for difficulty menu",
            WIDTH // 2, 405, GREY, small_font, center=True
        )

    pygame.display.flip()

pygame.quit()
