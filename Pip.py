
import math
import random
import sys
import pygame
import numpy as np

pygame.init()

# Window setup
W, H = 1000, 700
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("CYBER CORE | Energy Reactor")
clock = pygame.time.Clock()

# Colors
BG = (5, 8, 20)
CYAN = (0, 240, 255)
BLUE = (50, 100, 255)
PURPLE = (175, 50, 255)
WHITE = (235, 250, 255)
GREEN = (30, 255, 150)
ORANGE = (255, 145, 40)

font = pygame.font.SysFont("consolas", 18)
big_font = pygame.font.SysFont("consolas", 32, bold=True)
small_font = pygame.font.SysFont("consolas", 13)

CENTER = (W // 2, H // 2 + 10)
running = True
time_value = 0.0
energy = 100.0
blast = 0.0
mouse_control = False
paused = False
sound_enabled = True
show_help = True

# Procedural sound: no external audio file needed
def make_sound(freq=440, duration=0.12, volume=0.18):
    try:
        sample_rate = 22050
        n = int(sample_rate * duration)
        t = np.arange(n) / sample_rate
        wave = np.sin(2 * np.pi * freq * t)
        envelope = np.linspace(1, 0, n) ** 2
        audio = (wave * envelope * volume * 32767).astype(np.int16)
        stereo = np.column_stack((audio, audio))
        return pygame.sndarray.make_sound(stereo.copy())
    except Exception:
        return None

try:
    pygame.mixer.init()
except pygame.error:
    pass

sounds = {
    "blast": make_sound(100, 0.35, 0.25),
    "click": make_sound(650, 0.08, 0.12),
    "power": make_sound(260, 0.18, 0.15)
}

def play(name):
    if sound_enabled and pygame.mixer.get_init():
        s = sounds.get(name)
        if s:
            s.play()

# Particles
class Particle:
    def __init__(self, burst=False):
        self.reset(burst)

    def reset(self, burst=False):
        angle = random.random() * math.tau
        radius = random.uniform(25, 330)
        self.x = CENTER[0] + math.cos(angle) * radius
        self.y = CENTER[1] + math.sin(angle) * radius

        if burst:
            self.x = CENTER[0]
            self.y = CENTER[1]
            speed = random.uniform(2, 10)
        else:
            speed = random.uniform(0.3, 2.0)

        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.size = random.randint(1, 3)
        self.life = random.randint(40, 150)
        self.color = random.choice([CYAN, BLUE, PURPLE, WHITE])

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1

        if self.life <= 0:
            self.reset()

    def draw(self):
        alpha_color = self.color
        pygame.draw.circle(
            screen,
            alpha_color,
            (int(self.x), int(self.y)),
            self.size
        )

particles = [Particle() for _ in range(180)]

# Background stars
stars = [
    (random.randrange(W), random.randrange(H),
     random.choice([1, 1, 2]))
    for _ in range(130)
]

def draw_text(text, x, y, color=CYAN, font_obj=font):
    image = font_obj.render(text, True, color)
    screen.blit(image, (x, y))

def draw_grid():
    for x in range(0, W, 50):
        pygame.draw.line(screen, (12, 24, 42), (x, 0), (x, H))
    for y in range(0, H, 50):
        pygame.draw.line(screen, (12, 24, 42), (0, y), (W, y))

def draw_ring(radius, angle, color, width=2, segments=100):
    points = []

    for i in range(segments + 1):
        a = math.tau * i / segments + angle
        x = CENTER[0] + math.cos(a) * radius
        y = CENTER[1] + math.sin(a) * radius * 0.48
        points.append((int(x), int(y)))

    pygame.draw.lines(screen, color, False, points, width)

def draw_reactor(t):
    cx, cy = CENTER
    pulse = 1 + 0.045 * math.sin(t * 3)
    radius = int(75 * pulse + blast * 0.25)

    # Outer orbit rings
    draw_ring(225, t * 0.35, (20, 70, 110), 2)
    draw_ring(190, -t * 0.55, BLUE, 2)
    draw_ring(150, t * 0.8, CYAN, 2)
    draw_ring(110, -t * 1.1, PURPLE, 2)

    # Rotating orbit markers
    for i in range(12):
        a = t * 0.7 + i * math.tau / 12
        x = cx + math.cos(a) * 190
        y = cy + math.sin(a) * 91

        pygame.draw.circle(
            screen, CYAN, (int(x), int(y)), 3
        )

    # Central glow
    for r, color in [
        (radius + 38, (12, 35, 75)),
        (radius + 25, (10, 70, 115)),
        (radius + 13, (0, 125, 170)),
    ]:
        pygame.draw.circle(screen, color, (cx, cy), r)

    pygame.draw.circle(screen, CYAN, (cx, cy), radius, 3)
    pygame.draw.circle(
        screen, (10, 35, 75), (cx, cy), radius - 5
    )

    # Core highlights
    for i in range(6):
        a = -t * 1.5 + i * math.tau / 6
        x = cx + math.cos(a) * radius * 0.63
        y = cy + math.sin(a) * radius * 0.63

        pygame.draw.circle(
            screen, WHITE, (int(x), int(y)), 4
        )

    pygame.draw.circle(
        screen, WHITE, (cx, cy), max(4, int(9 * pulse))
    )

    # Reactor label
    draw_text(
        "CORE-" + str(int(energy)).zfill(3),
        cx - 54, cy + radius + 15, WHITE
    )

def draw_energy_bar():
    x, y, width, height = 35, 120, 190, 15

    pygame.draw.rect(
        screen, (25, 40, 60), (x, y, width, height)
    )

    fill = int(width * max(0, energy) / 100)

    if fill > 0:
        color = GREEN if energy > 25 else ORANGE
        pygame.draw.rect(
            screen, color, (x, y, fill, height)
        )

    pygame.draw.rect(
        screen, CYAN, (x, y, width, height), 1
    )

def trigger_blast():
    global blast, energy, particles

    if energy >= 15:
        energy -= 15
        blast = 100
        for _ in range(70):
            particles.append(Particle(burst=True))
        play("blast")

def draw_hud():
    draw_text("C Y B E R   C O R E", 30, 25, CYAN, big_font)
    draw_text("QUANTUM REACTOR // SYSTEM ONLINE", 32, 65, WHITE)

    draw_text("ENERGY LEVEL", 35, 95)
    draw_energy_bar()
    draw_text(f"{energy:05.1f}%", 235, 118, GREEN)

    draw_text("PARTICLES", 35, 165, WHITE)
    draw_text(str(len(particles)), 145, 165, CYAN)

    draw_text(
        "STATUS: " + ("PAUSED" if paused else "STABLE"),
        35, 190, ORANGE if paused else GREEN
    )

    draw_text("SYSTEM TELEMETRY", W - 250, 30, PURPLE)

    draw_text(f"TIME: {time_value:07.1f}s", W - 250, 60, WHITE)
    draw_text(f"FREQUENCY: {int(420 + 40 * math.sin(time_value))} Hz",
              W - 250, 85, CYAN)
    draw_text(f"CORE TEMP: {int(300 + 30 * math.sin(time_value * 0.7))} K",
              W - 250, 110, ORANGE)

    draw_text("CONTROLS", 35, H - 145, PURPLE)
    draw_text("[SPACE]  ENERGY BLAST", 35, H - 118, WHITE)
    draw_text("[UP]     RECHARGE ENERGY", 35, H - 95, WHITE)
    draw_text("[M]      SOUND ON/OFF", 35, H - 72, WHITE)
    draw_text("[P]      PAUSE / RESUME", 35, H - 49, WHITE)
    draw_text("[H]      HELP / HIDE", 35, H - 26, WHITE)

    draw_text("PYTHON // PYGAME ENGINE", W - 250, H - 30, CYAN)

# Main loop
while running:
    dt = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            elif event.key == pygame.K_SPACE and not paused:
                trigger_blast()

            elif event.key == pygame.K_UP and not paused:
                old_energy = energy
                energy = min(100, energy + 10)
                if energy > old_energy:
                    play("power")

            elif event.key == pygame.K_p:
                paused = not paused
                play("click")

            elif event.key == pygame.K_m:
                sound_enabled = not sound_enabled

            elif event.key == pygame.K_h:
                show_help = not show_help

            elif event.key == pygame.K_r:
                energy = 100
                blast = 0
                particles = [Particle() for _ in range(180)]

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and not paused:
                trigger_blast()

    if not paused:
        time_value += dt
        blast = max(0, blast - 2.5)

        # Gradually restore energy
        energy = min(100, energy + 0.8 * dt)

        for particle in particles:
            particle.update()

        # Remove extra burst particles after they leave the scene
        particles = [
            p for p in particles
            if -20 < p.x < W + 20 and -20 < p.y < H + 20
        ]

    screen.fill(BG)
    draw_grid()

    for x, y, size in stars:
        brightness = int(
            90 + 100 * (0.5 + 0.5 * math.sin(time_value + x))
        )
        pygame.draw.circle(
            screen,
            (brightness // 4, brightness // 2, brightness),
            (x, y),
            size
        )

    for particle in particles:
        particle.draw()

    draw_reactor(time_value)

    # Blast wave
    if blast > 0:
        blast_radius = int((100 - blast) * 4 + 20)
        pygame.draw.circle(
            screen, CYAN, CENTER, blast_radius, 2
        )

    draw_hud()

    if show_help:
        pygame.draw.rect(
            screen, (8, 17, 38), (W // 2 - 145, H - 78, 300, 36)
        )
        pygame.draw.rect(
            screen, BLUE, (W // 2 - 145, H - 78, 300, 36), 1
        )
        draw_text(
            "PRESS SPACE TO RELEASE ENERGY",
            W // 2 - 130, H - 67, WHITE, small_font
        )

    pygame.display.flip()

pygame.quit()
sys.exit()
