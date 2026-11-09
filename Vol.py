
import pygame
import random
import math
import sys

pygame.init()

# ---------------- WINDOW ----------------
WIDTH, HEIGHT = 1100, 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("VOLCANO - Eruption Simulator")

clock = pygame.time.Clock()
FPS = 60

# ---------------- COLORS ----------------
BLACK = (8, 9, 17)
DARK = (20, 18, 27)
ROCK = (65, 53, 53)
ROCK_LIGHT = (100, 76, 65)
ORANGE = (255, 90, 10)
YELLOW = (255, 190, 25)
RED = (210, 35, 8)
WHITE = (255, 240, 210)

title_font = pygame.font.SysFont("Arial", 38, bold=True)
font = pygame.font.SysFont("Arial", 19)
small_font = pygame.font.SysFont("Arial", 15)

canvas = pygame.Surface((WIDTH, HEIGHT))

# ---------------- BACKGROUND ----------------

background = pygame.Surface((WIDTH, HEIGHT))

for y in range(HEIGHT):
    ratio = y / HEIGHT

    color = (
        int(12 + ratio * 10),
        int(13 + ratio * 4),
        int(26 - ratio * 10)
    )

    pygame.draw.line(background, color, (0, y), (WIDTH, y))

# Stars
stars = []

for i in range(110):
    stars.append((
        random.randint(0, WIDTH),
        random.randint(0, 400),
        random.randint(1, 2)
    ))

# ---------------- MOUNTAIN ----------------

mountain_points = [
    (0, 690),
    (110, 610),
    (210, 510),
    (300, 415),
    (370, 345),
    (425, 310),
    (460, 325),
    (480, 342),
    (500, 347),
    (520, 342),
    (540, 325),
    (575, 310),
    (630, 345),
    (710, 420),
    (800, 520),
    (920, 610),
    (1100, 690)
]

# Rock texture points
random.seed(20)
rocks = []

for i in range(180):
    x = random.randint(50, 1050)
    y = random.randint(370, 680)

    rocks.append((
        x, y,
        random.randint(2, 5),
        random.choice([ROCK_LIGHT, (48, 40, 42), (75, 59, 55)])
    ))

# ---------------- LAVA PATHS ----------------

lava_paths = [
    [(485, 340), (450, 385), (420, 435),
     (390, 495), (355, 550), (320, 620)],

    [(515, 340), (550, 385), (575, 435),
     (610, 490), (650, 555), (700, 625)],

    [(490, 345), (475, 400), (480, 455),
     (460, 520), (450, 600)],

    [(520, 345), (540, 405), (550, 465),
     (585, 535), (610, 615)]
]


# ---------------- PARTICLES ----------------

class Particle:

    def __init__(self, x, y, kind="lava"):

        self.x = x
        self.y = y

        self.kind = kind

        if kind == "smoke":
            self.vx = random.uniform(-0.7, 0.7)
            self.vy = random.uniform(-2.0, -0.7)
            self.radius = random.randint(15, 35)
            self.life = random.randint(100, 180)

        elif kind == "ash":
            self.vx = random.uniform(-1.5, 1.5)
            self.vy = random.uniform(-2.5, -0.5)
            self.radius = random.randint(2, 5)
            self.life = random.randint(100, 200)

        else:
            self.vx = random.uniform(-3, 3)
            self.vy = random.uniform(-8, -2)
            self.radius = random.randint(3, 7)
            self.life = random.randint(35, 75)

        self.max_life = self.life

    def update(self):

        self.x += self.vx
        self.y += self.vy

        self.vy += 0.035

        if self.kind == "smoke":
            self.radius += 0.12

        self.life -= 1

    def draw(self, surface):

        if self.life <= 0:
            return

        if self.kind == "smoke":

            alpha = int(65 * self.life / self.max_life)

            smoke_surface = pygame.Surface(
                (int(self.radius * 2 + 4),
                 int(self.radius * 2 + 4)),
                pygame.SRCALPHA
            )

            pygame.draw.circle(
                smoke_surface,
                (125, 119, 125, alpha),
                (int(self.radius + 2), int(self.radius + 2)),
                int(self.radius)
            )

            surface.blit(
                smoke_surface,
                (int(self.x - self.radius),
                 int(self.y - self.radius))
            )

        elif self.kind == "ash":

            pygame.draw.circle(
                surface,
                (100, 92, 91),
                (int(self.x), int(self.y)),
                self.radius
            )

        else:

            pygame.draw.circle(
                surface,
                random.choice([ORANGE, YELLOW, RED]),
                (int(self.x), int(self.y)),
                self.radius
            )


particles = []


# ---------------- HELPERS ----------------

def draw_lava(surface, path, pulse):

    # Outer glowing stream
    pygame.draw.lines(
        surface,
        (110, 30, 5),
        False,
        path,
        29
    )

    # Orange lava
    pygame.draw.lines(
        surface,
        ORANGE,
        False,
        path,
        19
    )

    # Bright molten center
    pygame.draw.lines(
        surface,
        YELLOW,
        False,
        path,
        6
    )

    # Animated glowing sections
    for i, point in enumerate(path):

        glow = 4 + abs(math.sin(pulse + i)) * 4

        pygame.draw.circle(
            surface,
            YELLOW,
            point,
            int(glow)
        )


def draw_volcano(surface, pulse):

    # Mountain body
    pygame.draw.polygon(
        surface,
        (38, 32, 34),
        mountain_points
    )

    # Mountain shading
    pygame.draw.polygon(
        surface,
        (68, 49, 45),
        [
            (0, 690),
            (425, 310),
            (460, 325),
            (370, 500),
            (240, 690)
        ]
    )

    # Rocky texture
    for x, y, radius, color in rocks:

        if y > 670:
            continue

        pygame.draw.circle(
            surface,
            color,
            (x, y),
            radius
        )

    # Rock cracks
    for i in range(20):

        x = 250 + i * 32
        y = 470 + int(math.sin(i * 2) * 60)

        pygame.draw.line(
            surface,
            (35, 27, 27),
            (x, y),
            (x + 15, y + 25),
            2
        )

    # Lava paths
    for path in lava_paths:
        draw_lava(surface, path, pulse)

    # Volcano crater
    pygame.draw.ellipse(
        surface,
        (30, 13, 10),
        (445, 300, 110, 52)
    )

    pygame.draw.ellipse(
        surface,
        (145, 40, 5),
        (457, 311, 86, 29)
    )

    pygame.draw.ellipse(
        surface,
        YELLOW,
        (476, 320, 48, 13)
    )


# ---------------- MAIN LOOP ----------------

running = True
paused = False

frame = 0
shake = 0

eruption_power = 1.0

while running:

    clock.tick(FPS)

    frame += 1

    # Events
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                running = False

            if event.key == pygame.K_SPACE:
                paused = not paused

            if event.key == pygame.K_r:
                particles.clear()
                frame = 0
                shake = 0

            if event.key == pygame.K_UP:
                eruption_power = min(3.0, eruption_power + 0.25)

            if event.key == pygame.K_DOWN:
                eruption_power = max(0.5, eruption_power - 0.25)

    if not paused:

        canvas.blit(background, (0, 0))

        # Stars
        for x, y, radius in stars:

            brightness = int(
                130 + 100 * abs(math.sin(frame * 0.02 + x))
            )

            pygame.draw.circle(
                canvas,
                (brightness, brightness, brightness),
                (x, y),
                radius
            )

        # Smoke generation
        if frame % max(1, int(4 / eruption_power)) == 0:

            for i in range(3):

                particles.append(
                    Particle(
                        random.randint(465, 535),
                        320,
                        "smoke"
                    )
                )

        # Ash generation
        if frame % 5 == 0:

            particles.append(
                Particle(
                    random.randint(460, 540),
                    325,
                    "ash"
                )
            )

        # Lava sparks
        if frame % max(1, int(3 / eruption_power)) == 0:

            for i in range(3):

                particles.append(
                    Particle(
                        random.randint(470, 530),
                        325,
                        "lava"
                    )
                )

        # Update particles
        for particle in particles[:]:

            particle.update()
            particle.draw(canvas)

            if particle.life <= 0:
                particles.remove(particle)

        # Volcano
        pulse = frame * 0.06

        draw_volcano(canvas, pulse)

        # Ground
        pygame.draw.rect(
            canvas,
            (18, 15, 18),
            (0, 690, WIDTH, 60)
        )

        # Ground glow
        pygame.draw.line(
            canvas,
            (100, 38, 8),
            (0, 690),
            (WIDTH, 690),
            3
        )

        # Eruption glow
        glow_radius = 90 + int(abs(math.sin(pulse)) * 25)

        glow = pygame.Surface(
            (WIDTH, HEIGHT),
            pygame.SRCALPHA
        )

        pygame.draw.circle(
            glow,
            (255, 65, 0, 18),
            (500, 335),
            glow_radius
        )

        canvas.blit(glow, (0, 0))

        # Screen shake effect
        shake = max(0, 5 * eruption_power *
                    abs(math.sin(frame * 0.15)))

        shake_x = random.randint(-int(shake), int(shake))
        shake_y = random.randint(-int(shake), int(shake))

        # HUD
        title = title_font.render(
            "VOLCANIC ERUPTION",
            True,
            (255, 170, 80)
        )

        canvas.blit(title, (30, 25))

        status = font.render(
            "STATUS: " + ("PAUSED" if paused else "ACTIVE"),
            True,
            WHITE
        )

        canvas.blit(status, (30, 80))

        power = font.render(
            f"ERUPTION INTENSITY: {eruption_power:.2f}x",
            True,
            ORANGE
        )

        canvas.blit(power, (30, 115))

        instructions = [
            "SPACE  : Pause / Resume",
            "R      : Reset",
            "UP     : Increase visual intensity",
            "DOWN   : Decrease visual intensity",
            "ESC    : Exit"
        ]

        for i, line in enumerate(instructions):

            text = small_font.render(
                line,
                True,
                (220, 210, 205)
            )

            canvas.blit(
                text,
                (790, 35 + i * 28)
            )

        # Bottom label
        label = small_font.render(
            "PYTHON VOLCANO SIMULATOR  |  PARTICLE ANIMATION",
            True,
            (200, 150, 120)
        )

        canvas.blit(
            label,
            (WIDTH // 2 - label.get_width() // 2, 720)
        )

        screen.fill(BLACK)

        screen.blit(
            canvas,
            (shake_x, shake_y)
        )

        pygame.display.flip()

    else:

        screen.blit(canvas, (0, 0))

        pause_text = title_font.render(
            "SIMULATION PAUSED",
            True,
            WHITE
        )

        screen.blit(
            pause_text,
            (
                WIDTH // 2 - pause_text.get_width() // 2,
                HEIGHT // 2
            )
        )

        pygame.display.flip()

pygame.quit()
sys.exit()
