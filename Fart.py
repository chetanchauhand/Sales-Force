
import pygame
import random
import math
import array

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()

W, H = 900, 600
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("😂 NAME FART GENERATOR 💨")
clock = pygame.time.Clock()

font = pygame.font.SysFont("comicsansms", 30, bold=True)
big_font = pygame.font.SysFont("comicsansms", 43, bold=True)
small_font = pygame.font.SysFont("comicsansms", 21, bold=True)

# Sound generator: different cartoon pitches and patterns
def create_sound(kind):
    rate = 22050
    duration = 0.85 if kind == "loud" else 0.35
    samples = array.array("h")
    phase = 0

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
        value = int(max(-32767, min(32767,
                                   volume * envelope * wave_value)))
        samples.append(value)

    return pygame.mixer.Sound(buffer=samples.tobytes())


sounds = {
    "loud": create_sound("loud"),
    "poin": create_sound("poin"),
    "bhu": create_sound("bhu"),
    "phat": create_sound("phat"),
}

sounds["loud"].set_volume(1.0)

# Input box
name = ""
active = True
result = "ENTER YOUR NAME!"
sound_label = "READY?"
particles = []
score = 0
shake = 0
result_timer = 0

input_box = pygame.Rect(250, 155, 400, 55)
button = pygame.Rect(330, 235, 240, 60)

def draw_text(text, font_obj, color, pos):
    image = font_obj.render(text, True, color)
    screen.blit(image, image.get_rect(center=pos))

def make_particles():
    for _ in range(65):
        particles.append([
            random.randint(410, 490),
            random.randint(340, 400),
            random.uniform(-4, 4),
            random.uniform(-5, 1),
            random.randint(25, 70),
            random.randint(8, 23)
        ])

def generate_fart():
    global result, sound_label, score, shake, result_timer

    person = name.strip().lower()

    if not person:
        result = "PEHLE NAAM LIKHO!"
        sound_label = "NO NAME"
        return

    # Chetan: special silent mode
    if person == "chetan":
        result = "CHETAN: SILENT MODE 🤫"
        sound_label = "NO SOUND!"
        result_timer = 120
        return

    # Priyanshu: loud cartoon sound
    elif person == "priyanshu":
        result = "PRIYANSHU: BHADAAAM! 💥"
        sound_label = "EXTRA LOUD FART!"
        sounds["loud"].play()
        shake = 15
        score += 100
        make_particles()

    # Everyone else gets a random funny sound
    else:
        kind = random.choice(["phat", "poin", "bhu"])
        sounds[kind].play()

        labels = {
            "phat": "PHATTT! 💨",
            "poin": "POINNN! 🎈",
            "bhu": "BHUUU! 💨"
        }

        result = f"{name.strip()}: {labels[kind]}"
        sound_label = "FUNNY SOUND!"
        shake = 5
        score += 10
        make_particles()

    result_timer = 120


running = True

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            active = input_box.collidepoint(event.pos)

            if button.collidepoint(event.pos):
                generate_fart()

        if event.type == pygame.KEYDOWN and active:
            if event.key == pygame.K_RETURN:
                generate_fart()
            elif event.key == pygame.K_BACKSPACE:
                name = name[:-1]
            elif event.unicode.isprintable() and len(name) < 22:
                name += event.unicode

    # Screen shake
    dx = random.randint(-shake, shake) if shake > 0 else 0
    shake = max(0, shake - 1)

    screen.fill((15, 20, 45))

    # Background circles
    for i in range(12):
        x = (i * 91 + 30) % W
        y = (i * 67 + 20) % H
        pygame.draw.circle(screen, (25, 35, 70),
                           (x, y), 20 + (i % 4) * 5, 2)

    draw_text("FUNNY FART GENERATOR", big_font,
              (100, 255, 150), (450 + dx, 55))

    draw_text("TYPE A NAME AND DISCOVER THE SOUND!",
              small_font, (230, 230, 255), (450, 100))

    # Name input box
    pygame.draw.rect(screen, (240, 245, 255), input_box,
                     border_radius=12)
    pygame.draw.rect(screen,
                     (70, 255, 140) if active else (130, 140, 180),
                     input_box, 3, border_radius=12)

    shown_name = name if name else "Enter name here..."
    color = (30, 35, 50) if name else (130, 130, 145)
    draw_text(shown_name, font, color, (450, 182))

    # Button
    pygame.draw.rect(screen, (30, 180, 90), button,
                     border_radius=15)
    pygame.draw.rect(screen, (120, 255, 180), button, 3,
                     border_radius=15)
    draw_text("MAKE FART! 💨", font,
              (255, 255, 255), (450, 265))

    # Results
    draw_text(result, font, (255, 225, 70), (450 + dx, 350))
    draw_text(sound_label, small_font,
              (100, 230, 255), (450, 395))

    # Gas particles
    for p in particles[:]:
        p[0] += p[2]
        p[1] += p[3]
        p[4] -= 1
        p[5] *= 0.985

        if p[4] <= 0 or p[5] < 2:
            particles.remove(p)
            continue

        color = random.choice([
            (100, 240, 80), (160, 255, 90),
            (80, 200, 100), (200, 255, 120)
        ])
        pygame.draw.circle(screen, color,
                           (int(p[0]), int(p[1])),
                           int(p[5]))

    draw_text(f"SCORE: {score}", small_font,
              (255, 220, 70), (780, 35))

    draw_text("ENTER = PLAY | CLICK = GENERATE",
              small_font, (220, 225, 245), (450, 550))

    draw_text("SILENT MODE AVAILABLE 🤫",
              small_font, (150, 180, 220), (450, 580))

    pygame.display.flip()

pygame.quit()
