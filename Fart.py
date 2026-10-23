
import pygame
import random
import math
import array

# ---------------- INITIALIZATION ----------------
pygame.mixer.pre_init(22050, -16, 1, 512)
pygame.init()

W, H = 900, 600
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("NAME FART GENERATOR - BOSS MODE")
clock = pygame.time.Clock()

font = pygame.font.SysFont("comicsansms", 30, bold=True)
big_font = pygame.font.SysFont("comicsansms", 43, bold=True)
small_font = pygame.font.SysFont("comicsansms", 21, bold=True)

# ---------------- SOUND GENERATOR ----------------
def create_sound(kind):
    rate = 22050
    duration = 0.85 if kind == "loud" else 0.35
    samples = array.array("h")
    phase = 0.0

    for i in range(int(rate * duration)):
        t = i / rate

        if kind == "loud":
            freq = 65 + 45 * math.sin(t * 32) + 20 * math.sin(t * 85)
            envelope = min(1, t * 35) * max(0, 1 - t / duration)
            noise = random.uniform(-1, 1) * 0.65
            volume = 26000

        elif kind == "poin":
            freq = 250 + 220 * math.sin(t * 15)
            envelope = max(0, 1 - t / duration)
            noise = 0
            volume = 14000

        elif kind == "bhu":
            freq = 90 + 35 * math.sin(t * 20)
            envelope = max(0, 1 - t / duration)
            noise = random.uniform(-1, 1) * 0.25
            volume = 18000

        else:
            freq = 125 + 65 * math.sin(t * 40)
            envelope = max(0, 1 - t / duration)
            noise = random.uniform(-1, 1) * 0.45
            volume = 17000

        phase += 2 * math.pi * freq / rate
        wave_value = math.sin(phase) * 0.65 + noise

        value = int(max(
            -32767,
            min(32767, volume * envelope * wave_value)
        ))
        samples.append(value)

    return pygame.mixer.Sound(buffer=samples.tobytes())


sounds = {
    "loud": create_sound("loud"),
    "poin": create_sound("poin"),
    "bhu": create_sound("bhu"),
    "phat": create_sound("phat"),
}

sounds["loud"].set_volume(1.0)

# ---------------- GAME VARIABLES ----------------
name = ""
active = True

result = "ENTER YOUR NAME!"
sound_label = "READY?"

particles = []
score = 0
coins = 0
combo = 0
shake = 0
result_timer = 0

challenge_messages = [
    "MEGA FART UNLOCKED!",
    "LEGENDARY PFFFT!",
    "COMBO MASTER!",
    "GAS POWER MAX!",
    "ULTIMATE BHURRR!"
]

last_challenge = "READY FOR CHALLENGE?"

input_box = pygame.Rect(250, 155, 400, 55)
button = pygame.Rect(330, 235, 240, 60)


# ---------------- DRAW TEXT ----------------
def draw_text(text, font_obj, color, pos):
    image = font_obj.render(text, True, color)
    screen.blit(image, image.get_rect(center=pos))


# ---------------- PARTICLES ----------------
def make_particles():
    for _ in range(65):
        particles.append([
            random.randint(410, 490),   # x
            random.randint(340, 400),   # y
            random.uniform(-4, 4),      # speed x
            random.uniform(-5, 1),      # speed y
            random.randint(25, 70),     # lifetime
            random.randint(8, 23)       # size
        ])


# ---------------- GENERATE RESULT ----------------
def generate_fart():
    global result, sound_label
    global score, coins, combo, shake, result_timer
    global last_challenge

    person = name.strip().casefold()

    # Empty name
    if not person:
        result = "PEHLE NAAM LIKHO!"
        sound_label = "NO NAME"
        result_timer = 120
        return

    # CHETAN = BOSS MODE
    # No sound, no particles, no score, no coins, no combo.
    if person == "chetan":
        pygame.mixer.stop()
        particles.clear()

        result = "CHETAN: BOSS MODE!"
        sound_label = "SILENT MODE - NO SOUND"
        shake = 0
        result_timer = 180
        return

    # PRIYANSHU = EXTRA LOUD MODE
    if person == "priyanshu":
        result = "PRIYANSHU: BHADAAAM!"
        sound_label = "EXTRA LOUD CARTOON SOUND"

        sounds["loud"].play()
        shake = 15
        score += 100
        coins += 5
        combo += 1
        make_particles()

    # OTHER NAMES = RANDOM MODE
    else:
        kind = random.choice(["phat", "poin", "bhu"])
        sounds[kind].play()

        labels = {
            "phat": "PHATTT!",
            "poin": "POINNN!",
            "bhu": "BHUUU!"
        }

        result = f"{name.strip()}: {labels[kind]}"
        sound_label = "FUNNY CARTOON SOUND"

        shake = 5
        score += 10
        coins += 5
        combo += 1
        make_particles()

    # CHALLENGE: every third successful non-Chetan turn
    if combo > 0 and combo % 3 == 0:
        score += 50
        coins += 20

        last_challenge = random.choice(challenge_messages)
        result = last_challenge
        sound_label = "CHALLENGE BONUS!"
        shake = 12
        make_particles()

    result_timer = 120


# ---------------- MAIN GAME LOOP ----------------
running = True

while running:
    clock.tick(60)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # Mouse controls
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button.collidepoint(event.pos):
                generate_fart()

            elif input_box.collidepoint(event.pos):
                active = True

            else:
                active = False

        # Keyboard controls
        elif event.type == pygame.KEYDOWN and active:

            if event.key == pygame.K_RETURN:
                generate_fart()

            elif event.key == pygame.K_BACKSPACE:
                name = name[:-1]

            elif event.unicode.isprintable() and len(name) < 22:
                name += event.unicode

    # ---------------- UPDATE PARTICLES ----------------
    for p in particles[:]:
        p[0] += p[2]
        p[1] += p[3]
        p[4] -= 1
        p[5] *= 0.985

        if p[4] <= 0 or p[5] < 2:
            particles.remove(p)

    # ---------------- SCREEN SHAKE ----------------
    dx = random.randint(-shake, shake) if shake > 0 else 0
    shake = max(0, shake - 1)

    # ---------------- BACKGROUND ----------------
    screen.fill((15, 20, 45))

    for i in range(12):
        x = (i * 91 + 30) % W
        y = (i * 67 + 20) % H

        pygame.draw.circle(
            screen,
            (25, 35, 70),
            (x, y),
            20 + (i % 4) * 5,
            2
        )

    # ---------------- TITLE ----------------
    draw_text(
        "FUNNY FART GENERATOR",
        big_font,
        (100, 255, 150),
        (450 + dx, 55)
    )

    draw_text(
        "TYPE A NAME AND DISCOVER THE SOUND!",
        small_font,
        (230, 230, 255),
        (450, 100)
    )

    # ---------------- NAME INPUT ----------------
    pygame.draw.rect(
        screen, (240, 245, 255), input_box, border_radius=12
    )

    border_color = (
        (70, 255, 140) if active else (130, 140, 180)
    )

    pygame.draw.rect(
        screen, border_color, input_box, 3, border_radius=12
    )

    shown_name = name if name else "Enter name here..."
    text_color = (30, 35, 50) if name else (130, 130, 145)

    draw_text(shown_name, font, text_color, (450, 182))

    # ---------------- BUTTON ----------------
    pygame.draw.rect(
        screen, (30, 180, 90), button, border_radius=15
    )

    pygame.draw.rect(
        screen, (120, 255, 180), button, 3, border_radius=15
    )

    draw_text(
        "GENERATE!",
        font,
        (255, 255, 255),
        (450, 265)
    )

    # ---------------- RESULT ----------------
    result_color = (255, 225, 70)

    if "CHETAN" in result or "BOSS MODE" in result:
        result_color = (180, 140, 255)
    elif "PRIYANSHU" in result:
        result_color = (255, 100, 100)

    draw_text(
        result,
        font,
        result_color,
        (450 + dx, 350)
    )

    draw_text(
        sound_label,
        small_font,
        (100, 230, 255),
        (450, 395)
    )

    # ---------------- DRAW PARTICLES ----------------
    for p in particles:
        particle_color = random.choice([
            (100, 240, 80),
            (160, 255, 90),
            (80, 200, 100),
            (200, 255, 120)
        ])

        pygame.draw.circle(
            screen,
            particle_color,
            (int(p[0]), int(p[1])),
            max(1, int(p[5]))
        )

    # ---------------- SCOREBOARD ----------------
    draw_text(
        f"SCORE: {score}",
        small_font,
        (255, 220, 70),
        (780, 30)
    )

    draw_text(
        f"COINS: {coins}",
        small_font,
        (255, 220, 70),
        (780, 58)
    )

    draw_text(
        f"COMBO: {combo}",
        small_font,
        (100, 230, 255),
        (100, 30)
    )

    draw_text(
        f"CHALLENGE: {last_challenge}",
        small_font,
        (200, 170, 255),
        (450, 475)
    )

    draw_text(
        "ENTER = PLAY | CLICK BUTTON = GENERATE",
        small_font,
        (220, 225, 245),
        (450, 550)
    )

    draw_text(
        "CHETAN = SILENT BOSS MODE",
        small_font,
        (150, 180, 220),
        (450, 580)
    )

    pygame.display.flip()

pygame.quit()

