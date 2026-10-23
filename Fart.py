
import pygame
import random
import math
import array

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()

W, H = 1000, 650
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("FART MAN SIMULATOR 💨")
clock = pygame.time.Clock()

# Generate funny sound without external audio files
def make_fart_sound(duration=0.38):
    rate = 22050
    samples = array.array("h")
    phase = 0

    for i in range(int(rate * duration)):
        t = i / rate
        envelope = (1 - t / duration) ** 0.7
        freq = 85 + 30 * math.sin(t * 35) + 15 * math.sin(t * 91)
        phase += 2 * math.pi * freq / rate

        noise = random.uniform(-1, 1)
        value = (math.sin(phase) * 0.65 + noise * 0.35)
        samples.append(int(10000 * envelope * value))

    return pygame.mixer.Sound(buffer=samples.tobytes())

fart_sound = make_fart_sound()
fart_sound.set_volume(0.7)

font = pygame.font.SysFont("comicsansms", 30, bold=True)
small = pygame.font.SysFont("comicsansms", 21, bold=True)
big = pygame.font.SysFont("comicsansms", 52, bold=True)

# Gas particles
particles = []
score = 0
gas_meter = 100
sound_on = True
running = True
fart_timer = 0
shake = 0
message = "PRESS SPACE OR CLICK FART!"
message_timer = 180

def text(msg, font_obj, color, pos):
    img = font_obj.render(msg, True, color)
    screen.blit(img, img.get_rect(center=pos))

def fart():
    global score, gas_meter, shake, message, message_timer

    if gas_meter >= 20:
        score += 10
        gas_meter -= 20
        shake = 12
        message = random.choice([
            "PRRRRRT!!!",
            "PFFFT! ",
            "WHO DID THAT?!",
            "FART ATTACK!",
            "PEEE-YOOO!"
        ])
        message_timer = 65

        for _ in range(45):
            particles.append([
                random.randint(420, 550),
                random.randint(395, 435),
                random.uniform(-3, 2),
                random.uniform(-4, 1),
                random.randint(35, 85),
                random.randint(12, 28)
            ])

        if sound_on:
            fart_sound.play()

def draw_person(offset):
    # Shadow
    pygame.draw.ellipse(screen, (175, 170, 150),
                        (325, 535, 330, 35))

    # Legs
    pygame.draw.line(screen, (35, 65, 160),
                     (420 + offset, 435), (390 + offset, 535), 32)
    pygame.draw.line(screen, (35, 65, 160),
                     (510 + offset, 435), (550 + offset, 535), 32)

    # Shoes
    pygame.draw.ellipse(screen, (35, 35, 45),
                        (350 + offset, 520, 75, 30))
    pygame.draw.ellipse(screen, (35, 35, 45),
                        (525 + offset, 520, 75, 30))

    # Body
    pygame.draw.ellipse(screen, (235, 65, 60),
                        (375 + offset, 315, 175, 150))

    # Arms
    pygame.draw.line(screen, (235, 65, 60),
                     (395 + offset, 350), (350 + offset, 420), 27)
    pygame.draw.line(screen, (235, 65, 60),
                     (530 + offset, 350), (565 + offset, 405), 27)

    # Hands
    pygame.draw.circle(screen, (255, 205, 160),
                       (350 + offset, 420), 16)
    pygame.draw.circle(screen, (255, 205, 160),
                       (565 + offset, 405), 16)

    # Head
    pygame.draw.circle(screen, (255, 205, 160),
                       (465 + offset, 255), 73)

    # Hair
    pygame.draw.arc(screen, (55, 35, 25),
                    (395 + offset, 190, 140, 90), 0, math.pi, 12)
    pygame.draw.circle(screen, (55, 35, 25),
                       (415 + offset, 208), 18)
    pygame.draw.circle(screen, (55, 35, 25),
                       (440 + offset, 192), 20)

    # Eyes
    pygame.draw.ellipse(screen, (255, 255, 255),
                        (428 + offset, 235, 20, 28))
    pygame.draw.ellipse(screen, (255, 255, 255),
                        (478 + offset, 235, 20, 28))
    pygame.draw.circle(screen, (25, 25, 25),
                       (440 + offset, 250), 6)
    pygame.draw.circle(screen, (25, 25, 25),
                       (490 + offset, 250), 6)

    # Nose and goofy mouth
    pygame.draw.circle(screen, (230, 140, 120),
                       (463 + offset, 265), 7)
    pygame.draw.ellipse(screen, (95, 20, 30),
                        (444 + offset, 278, 43, 28))
    pygame.draw.arc(screen, (255, 255, 255),
                    (451 + offset, 280, 28, 13), 0, math.pi, 3)

def draw_cloud(x, y, size, alpha_color):
    color = alpha_color
    for dx, dy, r in [
        (0, 0, 1), (-0.6, 0.15, 0.7),
        (0.55, 0.15, 0.8), (-0.2, -0.45, 0.65),
        (0.35, -0.4, 0.6)
    ]:
        pygame.draw.circle(
            screen, color,
            (int(x + dx * size), int(y + dy * size)),
            max(1, int(r * size))
        )

while running:
    dt = clock.tick(60)
    fart_timer += dt

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                fart()
            elif event.key == pygame.K_s:
                sound_on = not sound_on
            elif event.key == pygame.K_r:
                score = 0
                gas_meter = 100
                particles.clear()
                message = "FRESH START!"
                message_timer = 90

        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.Rect(35, 530, 190, 65).collidepoint(event.pos):
                fart()
            elif pygame.Rect(35, 600, 190, 35).collidepoint(event.pos):
                sound_on = not sound_on

    # Background
    screen.fill((135, 205, 245))

    # Clouds and sun
    pygame.draw.circle(screen, (255, 230, 100), (850, 100), 55)
    for x, y in [(130, 100), (730, 190), (270, 175)]:
        pygame.draw.circle(screen, (255, 255, 255), (x, y), 27)
        pygame.draw.circle(screen, (255, 255, 255), (x+25, y-10), 32)
        pygame.draw.circle(screen, (255, 255, 255), (x+50, y), 24)

    # Ground
    pygame.draw.rect(screen, (100, 195, 100), (0, 555, W, 95))

    # Refill gas meter
    if gas_meter < 100 and fart_timer > 500:
        gas_meter = min(100, gas_meter + 0.025 * dt)

    # Camera shake
    offset = random.randint(-shake, shake) if shake > 0 else 0
    shake = max(0, shake - 1)

    draw_person(offset)

    # Cartoon gas clouds
    for p in particles[:]:
        p[0] += p[2]
        p[1] += p[3]
        p[4] -= 1
        p[5] *= 0.99

        if p[4] <= 0 or p[5] < 2:
            particles.remove(p)
            continue

        green = random.choice([
            (100, 215, 55), (135, 230, 65),
            (75, 185, 65), (175, 225, 75)
        ])
        draw_cloud(p[0], p[1], p[5], green)

    # Funny popup
    if message_timer > 0:
        message_timer -= 1
        text(message, big, (40, 70, 30), (500, 85))

    # Score panel
    pygame.draw.rect(screen, (30, 35, 55), (760, 20, 210, 85),
                     border_radius=18)
    text(f"SCORE: {score}", font, (255, 230, 80), (865, 62))

    # Gas meter
    pygame.draw.rect(screen, (35, 45, 60), (30, 25, 250, 35),
                     border_radius=10)
    pygame.draw.rect(screen, (80, 225, 80),
                     (35, 30, int(240 * gas_meter / 100), 25),
                     border_radius=8)
    text("FART POWER", small, (30, 50, 35), (145, 80))

    # Buttons
    pygame.draw.rect(screen, (30, 135, 55), (35, 530, 190, 65),
                     border_radius=16)
    text("💨 FART!", font, (255, 255, 255), (130, 562))

    pygame.draw.rect(screen, (40, 45, 65), (35, 600, 190, 35),
                     border_radius=10)
    text("SOUND: ON" if sound_on else "SOUND: OFF",
         small, (255, 255, 255), (130, 617))

    text("SPACE = FART     S = SOUND     R = RESET",
         small, (35, 45, 55), (600, 615))

    pygame.display.flip()

pygame.quit()
