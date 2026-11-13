
import pygame
import math
import random
import os

# ---------------- INITIALIZATION ----------------
pygame.init()

WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Divine Solar System - Navgraha Universe")

clock = pygame.time.Clock()

WHITE = (255, 255, 255)
GOLD = (255, 190, 50)
BG = (5, 5, 25)

font = pygame.font.SysFont("segoeui", 19, bold=True)
small_font = pygame.font.SysFont("segoeui", 16)
title_font = pygame.font.SysFont("segoeui", 32, bold=True)

CENTER_X, CENTER_Y = 430, 405

# ---------------- LOAD IMAGES ----------------
def load_image(filename, size):
    path = os.path.join("assets", filename)

    try:
        image = pygame.image.load(path).convert_alpha()
        return pygame.transform.smoothscale(image, (size, size))
    except (pygame.error, FileNotFoundError):
        return None


# ---------------- DEVTA INFORMATION ----------------
devtas = [
    {
        "name": "Chandra Dev",
        "image": "chandra.png",
        "orbit": 105,
        "speed": 0.65,
        "angle": 0,
        "color": (190, 210, 255),
        "description": "The deity associated with the Moon.",
        "detail": "Chandra Dev represents the Moon."
    },
    {
        "name": "Mangal Dev",
        "image": "mangal.png",
        "orbit": 145,
        "speed": 0.48,
        "angle": 45,
        "color": (255, 90, 65),
        "description": "The deity associated with Mars.",
        "detail": "Mangal Dev is associated with courage."
    },
    {
        "name": "Budh Dev",
        "image": "budh.png",
        "orbit": 185,
        "speed": 0.38,
        "angle": 100,
        "color": (100, 255, 140),
        "description": "The deity associated with Mercury.",
        "detail": "Budh Dev is associated with intelligence."
    },
    {
        "name": "Brihaspati Dev",
        "image": "brihaspati.png",
        "orbit": 225,
        "speed": 0.29,
        "angle": 155,
        "color": (255, 200, 80),
        "description": "The deity associated with Jupiter.",
        "detail": "Brihaspati Dev is the Guru of the Devas."
    },
    {
        "name": "Shukra Dev",
        "image": "shukra.png",
        "orbit": 265,
        "speed": 0.23,
        "angle": 205,
        "color": (255, 180, 220),
        "description": "The deity associated with Venus.",
        "detail": "Shukra Dev is the Guru of the Asuras."
    },
    {
        "name": "Shani Dev",
        "image": "shani.png",
        "orbit": 305,
        "speed": 0.17,
        "angle": 260,
        "color": (150, 160, 210),
        "description": "The deity associated with Saturn.",
        "detail": "Shani Dev is associated with karma."
    },
    {
        "name": "Rahu Dev",
        "image": "rahu.png",
        "orbit": 340,
        "speed": 0.12,
        "angle": 310,
        "color": (180, 100, 255),
        "description": "One of the lunar nodes.",
        "detail": "Rahu is one of the Navgrahas."
    },
    {
        "name": "Ketu Dev",
        "image": "ketu.png",
        "orbit": 370,
        "speed": 0.09,
        "angle": 350,
        "color": (150, 220, 190),
        "description": "The other lunar node.",
        "detail": "Ketu is one of the Navgrahas."
    }
]

# Load deity images
for devta in devtas:
    devta["picture"] = load_image(devta["image"], 64)

surya_image = load_image("surya.png", 135)

# ---------------- BACKGROUND STARS ----------------
stars = []

for i in range(250):
    stars.append({
        "x": random.randint(0, WIDTH),
        "y": random.randint(0, HEIGHT),
        "size": random.choice([1, 1, 2, 3]),
        "brightness": random.randint(100, 255),
        "phase": random.random() * 6.28
    })


def draw_stars():
    for star in stars:
        brightness = int(
            star["brightness"] *
            (0.65 + 0.35 * math.sin(pygame.time.get_ticks() / 600
                                    + star["phase"]))
        )

        brightness = max(0, min(255, brightness))

        pygame.draw.circle(
            screen,
            (brightness, brightness, brightness),
            (star["x"], star["y"]),
            star["size"]
        )


# ---------------- GLOW EFFECT ----------------
def draw_glow(x, y, radius, color):
    for i in range(5, 0, -1):
        alpha_surface = pygame.Surface(
            (radius * 4, radius * 4), pygame.SRCALPHA
        )

        pygame.draw.circle(
            alpha_surface,
            (*color, 18),
            (radius * 2, radius * 2),
            radius + i * 10
        )

        screen.blit(
            alpha_surface,
            (x - radius * 2, y - radius * 2)
        )


# ---------------- DRAW ORBITS ----------------
def draw_orbits():
    for devta in devtas:
        pygame.draw.circle(
            screen,
            (45, 55, 100),
            (CENTER_X, CENTER_Y),
            devta["orbit"],
            1
        )


# ---------------- DRAW SURYA DEV ----------------
def draw_surya():
    t = pygame.time.get_ticks()

    pulse = 7 * math.sin(t / 500)

    draw_glow(
        CENTER_X,
        CENTER_Y,
        int(65 + pulse),
        GOLD
    )

    pygame.draw.circle(
        screen,
        (255, 160, 20),
        (CENTER_X, CENTER_Y),
        67 + int(pulse)
    )

    if surya_image:
        rect = surya_image.get_rect(
            center=(CENTER_X, CENTER_Y)
        )
        screen.blit(surya_image, rect)
    else:
        pygame.draw.circle(
            screen, (255, 210, 40),
            (CENTER_X, CENTER_Y), 55
        )

        text = font.render("SURYA", True, (100, 35, 0))
        screen.blit(text, text.get_rect(center=(CENTER_X, CENTER_Y)))

    label = font.render("SURYA DEV", True, GOLD)
    screen.blit(
        label,
        label.get_rect(center=(CENTER_X, CENTER_Y + 95))
    )


# ---------------- DRAW DEVTA ----------------
def draw_devta(devta):
    angle = math.radians(devta["angle"])

    x = CENTER_X + math.cos(angle) * devta["orbit"]
    y = CENTER_Y + math.sin(angle) * devta["orbit"]

    devta["position"] = (int(x), int(y))

    draw_glow(int(x), int(y), 20, devta["color"])

    if devta["picture"]:
        rect = devta["picture"].get_rect(center=(int(x), int(y)))
        screen.blit(devta["picture"], rect)
    else:
        pygame.draw.circle(
            screen, devta["color"], (int(x), int(y)), 19
        )
        pygame.draw.circle(
            screen, WHITE, (int(x), int(y)), 19, 2
        )

    name = small_font.render(devta["name"], True, WHITE)

    screen.blit(
        name,
        name.get_rect(center=(int(x), int(y) + 42))
    )


# ---------------- INFORMATION PANEL ----------------
selected = None

def draw_information():
    panel = pygame.Rect(865, 125, 305, 535)

    pygame.draw.rect(
        screen, (15, 20, 48), panel, border_radius=18
    )

    pygame.draw.rect(
        screen, (80, 100, 160), panel,
        width=2, border_radius=18
    )

    heading = title_font.render("DIVINE WORLD", True, GOLD)
    screen.blit(heading, (890, 150))

    pygame.draw.line(
        screen, GOLD, (890, 200), (1145, 200), 2
    )

    if selected is None:
        lines = [
            "NAVGRAHA UNIVERSE",
            "",
            "Welcome to the Divine",
            "Solar System.",
            "",
            "Click any Devta to",
            "explore information.",
            "",
            "Surya Dev is at the",
            "centre of this universe."
        ]
    else:
        lines = [
            selected["name"],
            "",
            selected["description"],
            "",
            selected["detail"],
            "",
            "Associated orbit:",
            str(selected["orbit"]),
            "",
            "Click another Devta",
            "to explore more."
        ]

    y = 235

    for line in lines:
        rendered = small_font.render(line, True, WHITE)
        screen.blit(rendered, (890, y))
        y += 31


# ---------------- MAIN TITLE ----------------
def draw_title():
    title = title_font.render(
        "DIVINE SOLAR SYSTEM",
        True,
        GOLD
    )

    screen.blit(
        title,
        title.get_rect(center=(WIDTH // 2, 45))
    )

    subtitle = small_font.render(
        "THE SACRED NAVGRAHA UNIVERSE",
        True,
        WHITE
    )

    screen.blit(
        subtitle,
        subtitle.get_rect(center=(WIDTH // 2, 82))
    )


# ---------------- CONTROLS ----------------
speed_multiplier = 1.0
paused = False

def draw_controls():
    text = small_font.render(
        "SPACE: Pause/Play   UP/DOWN: Speed   ESC: Exit",
        True,
        (180, 190, 220)
    )

    screen.blit(text, (30, HEIGHT - 35))


# ---------------- MAIN LOOP ----------------
running = True

while running:

    clock.tick(60)

    screen.fill(BG)

    draw_stars()
    draw_title()
    draw_orbits()
    draw_surya()

    # Animate all Navgraha
    for devta in devtas:

        if not paused:
            devta["angle"] += devta["speed"] * speed_multiplier

        draw_devta(devta)

    draw_information()
    draw_controls()

    # Event handling
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                running = False

            elif event.key == pygame.K_SPACE:
                paused = not paused

            elif event.key == pygame.K_UP:
                speed_multiplier = min(5, speed_multiplier + 0.2)

            elif event.key == pygame.K_DOWN:
                speed_multiplier = max(0.2, speed_multiplier - 0.2)

        if event.type == pygame.MOUSEBUTTONDOWN:

            mx, my = pygame.mouse.get_pos()

            selected = None

            for devta in devtas:

                x, y = devta["position"]

                distance = math.sqrt(
                    (mx - x) ** 2 + (my - y) ** 2
                )

                if distance < 38:
                    selected = devta
                    break

    pygame.display.flip()


pygame.quit()
