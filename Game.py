import pygame
import math
import random
import numpy as np

pygame.init()
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)

WIDTH, HEIGHT = 900, 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lusty Animation - Boobs → Lund → Chut → Nude Ladki")

clock = pygame.time.Clock()
FPS = 60

# Colors
BG = (18, 8, 12)
SKIN = (255, 210, 180)
NIPPLE_PINK = (220, 90, 90)
NIPPLE_RED = (180, 40, 40)
DARK_NIPPLE = (140, 30, 30)
MILK = (255, 255, 240)
DICK = (255, 200, 170)
DICK_DARK = (70, 40, 30)          # Kala/Nigro lund
BALL = (240, 190, 160)
BALL_DARK = (60, 35, 25)
CUM = (255, 255, 230)
PANI = (255, 210, 230)
BUTTON = (160, 40, 70)
BUTTON_HOVER = (210, 60, 100)
BUTTON_GLOW = (255, 130, 160)
TEXT = (255, 180, 200)

font = pygame.font.SysFont("Arial", 26, bold=True)
small_font = pygame.font.SysFont("Arial", 18)

# ==================== SYNTHETIC MOAN ====================
def generate_moan(duration=0.55, sample_rate=22050):
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    freq = 380 - 160 * t
    wave = 0.38 * np.sin(2 * np.pi * freq * t)
    wave += 0.12 * np.sin(2 * np.pi * freq * 1.4 * t)
    wave += 0.06 * np.sin(2 * np.pi * freq * 2.1 * t)
    envelope = np.sin(np.pi * t / duration) ** 1.1
    wave *= envelope
    wave += 0.02 * np.random.normal(0, 1, len(t)) * envelope
    wave = np.clip(wave, -1, 1)
    sound_array = (wave * 32767).astype(np.int16)
    stereo = np.column_stack((sound_array, sound_array))
    return pygame.sndarray.make_sound(stereo)

try:
    moan_sound = generate_moan()
    moan_sound.set_volume(0.75)
except:
    moan_sound = None

# ==================== PARTICLES ====================
class Particle:
    def __init__(self, x, y, color, velocity=None, life=60):
        self.x = x
        self.y = y
        self.color = color
        self.vx = velocity[0] if velocity else random.uniform(-3, 3)
        self.vy = velocity[1] if velocity else random.uniform(-8, -2)
        self.life = life
        self.max_life = life
        self.size = random.randint(3, 8)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.25
        self.life -= 1
        self.size = max(1, self.size * 0.98)

    def draw(self, surface):
        alpha = int(255 * (self.life / self.max_life))
        s = pygame.Surface((self.size*2, self.size*2), pygame.SRCALPHA)
        pygame.draw.circle(s, (*self.color, alpha), (self.size, self.size), self.size)
        surface.blit(s, (self.x - self.size, self.y - self.size))

particles = []

# ==================== BOOBS ====================
class Boob:
    def __init__(self, x, y, base_radius):
        self.x = x
        self.y = y
        self.base_radius = base_radius
        self.radius = base_radius
        self.offset_y = 0
        self.vel_y = 0
        self.jiggle = 0

    def update(self, mouse_pos, mouse_pressed):
        mx, my = mouse_pos
        dist = math.hypot(mx - self.x, my - (self.y + self.offset_y))
        if dist < self.radius + 20 and mouse_pressed:
            self.jiggle = 14
            self.vel_y = -7
            for _ in range(4):
                angle = random.uniform(-0.8, 0.8)
                speed = random.uniform(4, 9)
                particles.append(Particle(
                    self.x + random.uniform(-10, 10),
                    self.y + self.offset_y + self.radius * 0.3,
                    MILK, (math.sin(angle)*speed, -math.cos(angle)*speed - 2), 50))
        self.vel_y += 0.55
        self.offset_y += self.vel_y
        self.vel_y *= 0.91
        self.vel_y -= self.offset_y * 0.09
        self.jiggle *= 0.9
        if self.jiggle < 0.4:
            self.jiggle = random.uniform(0.6, 1.8)
        self.radius = self.base_radius + math.sin(pygame.time.get_ticks()*0.005 + self.x)*2.5 + self.jiggle*0.5

    def draw(self, surface):
        pygame.draw.circle(surface, SKIN, (int(self.x), int(self.y + self.offset_y)), int(self.radius))
        pygame.draw.circle(surface, (255, 230, 200),
                           (int(self.x - self.radius*0.22), int(self.y + self.offset_y - self.radius*0.28)),
                           int(self.radius * 0.32))
        nipple_y = self.y + self.offset_y + self.radius * 0.22
        pygame.draw.circle(surface, NIPPLE_PINK, (int(self.x), int(nipple_y)), int(self.radius * 0.17))
        pygame.draw.circle(surface, DARK_NIPPLE, (int(self.x), int(nipple_y)), int(self.radius * 0.08))

# ==================== DICK (UPDATED) ====================
class Dick:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2 + 40
        self.base_length = 180
        self.base_width = 48
        self.shaft_length = 180
        self.shaft_width = 48
        self.ball_radius = 42
        self.stroke = 0
        self.stroking = False
        self.stroke_speed = 0
        self.cumming = False
        self.cum_timer = 0
        self.ball_press = 0
        self.press_count = 0          # Kitni baar balls dabaye
        self.press_cooldown = 0
        self.is_dark = False          # Kala lund active?
        self.super_cum = False        # 6th press pe strong cum

    def update(self, mouse_pos, mouse_pressed):
        mx, my = mouse_pos
        left_ball_x = self.x - 50
        right_ball_x = self.x + 50
        ball_y = self.y + 35

        dist_left = math.hypot(mx - left_ball_x, my - ball_y)
        dist_right = math.hypot(mx - right_ball_x, my - ball_y)

        if (dist_left < self.ball_radius + 18 or dist_right < self.ball_radius + 18) and mouse_pressed:
            self.ball_press = 14

            if self.press_cooldown <= 0:
                self.press_count += 1
                self.press_cooldown = 25   # Count properly

                # 5 baar pe kala + bada
                if self.press_count >= 5:
                    self.is_dark = True
                    self.shaft_length = 260          # Lamba
                    self.shaft_width = 68            # Mota (12 inch feel)
                    self.ball_radius = 52

                # 6 baar pe super favara
                if self.press_count >= 6:
                    self.super_cum = True
                    self.cumming = True
                    self.cum_timer = 140
                    self.stroking = False

                if not self.stroking and not self.cumming and self.press_count < 6:
                    self.stroking = True
                    self.stroke_speed = 0.09

        self.ball_press = max(0, self.ball_press - 0.7)
        self.press_cooldown = max(0, self.press_cooldown - 1)

        if self.stroking:
            self.stroke += self.stroke_speed
            if self.stroke >= 1:
                self.stroke = 1
                self.stroke_speed = -0.1
            elif self.stroke <= 0:
                self.stroke = 0
                self.stroke_speed = 0.09
                if random.random() < 0.2 and not self.super_cum:
                    self.stroking = False
                    self.cumming = True
                    self.cum_timer = 90

        if self.cumming:
            self.cum_timer -= 1
            tip_y = self.y - self.shaft_length + 15

            if self.super_cum:
                # Zor ka favara + real sperm jaisa
                if self.cum_timer > 40:
                    for _ in range(7):
                        particles.append(Particle(
                            self.x + random.uniform(-12, 12),
                            tip_y,
                            CUM,
                            (random.uniform(-4, 4), random.uniform(-16, -8)),
                            life=90
                        ))
            else:
                if self.cum_timer > 40:
                    for _ in range(3):
                        particles.append(Particle(
                            self.x + random.uniform(-8, 8),
                            tip_y,
                            CUM,
                            (random.uniform(-2.5, 2.5), random.uniform(-11, -5)),
                            life=70
                        ))

            if self.cum_timer <= 0:
                self.cumming = False
                self.super_cum = False

    def draw(self, surface):
        # Colors decide
        dick_color = DICK_DARK if self.is_dark else DICK
        ball_color = BALL_DARK if self.is_dark else BALL
        head_color = (50, 25, 20) if self.is_dark else (255, 180, 150)
        head_dark = (30, 15, 12) if self.is_dark else (240, 140, 120)

        ball_y = self.y + 35
        press_offset = self.ball_press * 0.9

        # Balls
        pygame.draw.circle(surface, ball_color, (self.x - 50, int(ball_y + press_offset)), self.ball_radius)
        pygame.draw.circle(surface, ball_color, (self.x + 50, int(ball_y + press_offset)), self.ball_radius)
        if not self.is_dark:
            pygame.draw.circle(surface, (255, 220, 190), (self.x - 60, int(ball_y - 12 + press_offset)), 15)
            pygame.draw.circle(surface, (255, 220, 190), (self.x + 40, int(ball_y - 12 + press_offset)), 15)

        # Shaft
        current_length = self.shaft_length * (0.87 + 0.13 * abs(math.sin(self.stroke * math.pi)))
        if self.cumming:
            current_length = self.shaft_length * 1.06

        shaft_top = self.y - current_length
        pygame.draw.rect(surface, dick_color,
                         (self.x - self.shaft_width//2, shaft_top, self.shaft_width, current_length),
                         border_radius=22)

        # Head
        pygame.draw.circle(surface, head_color, (self.x, int(shaft_top + 12)), self.shaft_width//2 + 6)
        pygame.draw.circle(surface, head_dark, (self.x, int(shaft_top + 12)), self.shaft_width//2 - 5)

        # Vein
        vein_color = (40, 20, 15) if self.is_dark else (220, 160, 140)
        pygame.draw.line(surface, vein_color,
                         (self.x - 10, shaft_top + 50),
                         (self.x - 6, self.y - 25), 4)

# ==================== CHUT ====================
class Chut:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2 + 30
        self.clit_x = self.x
        self.clit_y = self.y - 70
        self.wet = 0
        self.pulse = 0
        self.sound_cooldown = 0

    def update(self, mouse_pos, mouse_pressed):
        mx, my = mouse_pos
        dist = math.hypot(mx - self.clit_x, my - self.clit_y)
        if dist < 28 and mouse_pressed:
            self.wet = 18
            self.pulse = 8
            for _ in range(6):
                particles.append(Particle(self.x + random.uniform(-18, 18), self.y + 25, PANI,
                                          (random.uniform(-2.5, 2.5), random.uniform(3, 9)), 65))
            if self.sound_cooldown <= 0 and moan_sound:
                moan_sound.play()
                self.sound_cooldown = 45
        self.wet = max(0, self.wet - 0.45)
        self.pulse = max(0, self.pulse - 0.3)
        self.sound_cooldown = max(0, self.sound_cooldown - 1)

    def draw(self, surface):
        pygame.draw.ellipse(surface, SKIN, (self.x - 75, self.y - 50, 150, 190))
        pygame.draw.ellipse(surface, (255, 175, 165), (self.x - 42, self.y - 25, 84, 150))
        if self.wet > 5:
            pygame.draw.ellipse(surface, (255, 200, 210), (self.x - 20, self.y + 10, 40, 60))
        pygame.draw.line(surface, (170, 70, 85), (self.x, self.y - 15), (self.x, self.y + 105), 5)
        clit_size = 13 + self.pulse * 0.7 + self.wet * 0.15
        pygame.draw.circle(surface, NIPPLE_PINK, (int(self.clit_x), int(self.clit_y)), int(clit_size))
        pygame.draw.circle(surface, DARK_NIPPLE, (int(self.clit_x), int(self.clit_y)), int(clit_size * 0.45))

# ==================== NUDE LADKI ====================
class NudeGirl:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2 + 20
        self.boob_size = 70
        self.nipple_presses = 0
        self.nipple_color = NIPPLE_PINK
        self.milk_active = False
        self.clit_presses = 0
        self.hole_open = 0
        self.orgasming = False
        self.orgasm_timer = 0
        self.body_shake = 0
        self.sound_cooldown = 0

    def update(self, mouse_pos, mouse_pressed):
        mx, my = mouse_pos
        left_nipple_x = self.x - 55
        right_nipple_x = self.x + 55
        nipple_y = self.y - 30

        dist_left = math.hypot(mx - left_nipple_x, my - nipple_y)
        dist_right = math.hypot(mx - right_nipple_x, my - nipple_y)

        if (dist_left < 28 or dist_right < 28) and mouse_pressed:
            if self.sound_cooldown <= 0:
                self.nipple_presses += 1
                self.sound_cooldown = 20
                if self.nipple_presses >= 5:
                    self.nipple_color = NIPPLE_RED
                    self.boob_size = min(110, 70 + (self.nipple_presses - 4) * 6)
                if self.nipple_presses >= 6:
                    self.milk_active = True
                if moan_sound and self.nipple_presses % 2 == 0:
                    moan_sound.play()

        if self.milk_active and mouse_pressed and (dist_left < 28 or dist_right < 28):
            for _ in range(3):
                side = -1 if dist_left < dist_right else 1
                particles.append(Particle(
                    self.x + side * 55 + random.uniform(-8, 8),
                    nipple_y + 10, MILK,
                    (random.uniform(-1.5, 1.5), random.uniform(-9, -4)), 55))

        clit_x = self.x
        clit_y = self.y + 95
        dist_clit = math.hypot(mx - clit_x, my - clit_y)
        if dist_clit < 26 and mouse_pressed:
            if self.sound_cooldown <= 0:
                self.clit_presses += 1
                self.sound_cooldown = 18
                self.hole_open = min(1.0, self.clit_presses / 5)
                if moan_sound:
                    moan_sound.play()
                if self.clit_presses >= 5 and not self.orgasming:
                    self.orgasming = True
                    self.orgasm_timer = 120
                    self.body_shake = 12

        if self.orgasming:
            self.orgasm_timer -= 1
            self.body_shake = max(0, self.body_shake - 0.15)
            if self.orgasm_timer > 30:
                for _ in range(4):
                    particles.append(Particle(
                        self.x + random.uniform(-20, 20),
                        self.y + 110, PANI,
                        (random.uniform(-4, 4), random.uniform(4, 11)), 70))
            if self.orgasm_timer <= 0:
                self.orgasming = False

        self.sound_cooldown = max(0, self.sound_cooldown - 1)

    def draw(self, surface):
        shake_x = random.uniform(-self.body_shake, self.body_shake) if self.body_shake > 0 else 0
        shake_y = random.uniform(-self.body_shake*0.6, self.body_shake*0.6) if self.body_shake > 0 else 0
        cx = self.x + shake_x
        cy = self.y + shake_y

        pygame.draw.circle(surface, SKIN, (int(cx), int(cy - 160)), 38)
        pygame.draw.circle(surface, (60, 30, 20), (int(cx), int(cy - 175)), 42)
        pygame.draw.circle(surface, SKIN, (int(cx), int(cy - 155)), 30)
        pygame.draw.rect(surface, SKIN, (cx - 35, cy - 125, 70, 90), border_radius=15)
        pygame.draw.ellipse(surface, SKIN, (cx - 55, cy - 40, 110, 90))

        pygame.draw.circle(surface, SKIN, (int(cx - 50), int(cy - 40)), int(self.boob_size))
        pygame.draw.circle(surface, SKIN, (int(cx + 50), int(cy - 40)), int(self.boob_size))
        pygame.draw.circle(surface, (255, 230, 200), (int(cx - 60), int(cy - 55)), int(self.boob_size*0.3))
        pygame.draw.circle(surface, (255, 230, 200), (int(cx + 40), int(cy - 55)), int(self.boob_size*0.3))

        nipple_r = 11 + (self.boob_size - 70) * 0.08
        pygame.draw.circle(surface, self.nipple_color, (int(cx - 50), int(cy - 30)), int(nipple_r))
        pygame.draw.circle(surface, self.nipple_color, (int(cx + 50), int(cy - 30)), int(nipple_r))
        pygame.draw.circle(surface, DARK_NIPPLE, (int(cx - 50), int(cy - 30)), int(nipple_r*0.45))
        pygame.draw.circle(surface, DARK_NIPPLE, (int(cx + 50), int(cy - 30)), int(nipple_r*0.45))

        pygame.draw.circle(surface, (220, 170, 150), (int(cx), int(cy + 25)), 4)
        pygame.draw.ellipse(surface, (255, 175, 165), (cx - 28, cy + 55, 56, 70))
        hole_width = 4 + self.hole_open * 16
        pygame.draw.ellipse(surface, (160, 60, 70), (cx - hole_width/2, cy + 75, hole_width, 28 + self.hole_open*15))
        clit_size = 9 + self.hole_open * 4
        pygame.draw.circle(surface, NIPPLE_PINK, (int(cx), int(cy + 68)), int(clit_size))
        pygame.draw.circle(surface, DARK_NIPPLE, (int(cx), int(cy + 68)), int(clit_size*0.4))

        pygame.draw.ellipse(surface, SKIN, (cx - 70, cy + 100, 50, 110))
        pygame.draw.ellipse(surface, SKIN, (cx + 20, cy + 100, 50, 110))

# ==================== BUTTON ====================
button_rect = pygame.Rect(WIDTH//2 - 130, HEIGHT - 78, 260, 54)

def draw_button(surface, text, hover):
    shadow = button_rect.move(4, 4)
    pygame.draw.rect(surface, (30, 5, 15), shadow, border_radius=16)
    color = BUTTON_HOVER if hover else BUTTON
    pygame.draw.rect(surface, color, button_rect, border_radius=16)
    border_color = BUTTON_GLOW if hover else (200, 90, 120)
    pygame.draw.rect(surface, border_color, button_rect, 3, border_radius=16)
    txt = font.render(text, True, (255, 255, 255))
    surface.blit(txt, (button_rect.centerx - txt.get_width()//2, button_rect.centery - txt.get_height()//2))

# ==================== MAIN ====================
left_boob = Boob(WIDTH//2 - 130, HEIGHT//2 - 40, 115)
right_boob = Boob(WIDTH//2 + 130, HEIGHT//2 - 40, 115)
dick = Dick()
chut = Chut()
girl = NudeGirl()

modes = ["boobs", "dick", "chut", "girl"]
mode_index = 0
mode = modes[mode_index]

running = True
while running:
    clock.tick(FPS)
    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()[0]
    hover_button = button_rect.collidepoint(mouse_pos)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if button_rect.collidepoint(event.pos):
                mode_index = (mode_index + 1) % 4
                mode = modes[mode_index]
                particles.clear()
                dick.stroking = False
                dick.cumming = False
                dick.stroke = 0
                dick.press_count = 0
                dick.is_dark = False
                dick.super_cum = False
                dick.shaft_length = 180
                dick.shaft_width = 48
                dick.ball_radius = 42
                chut.wet = 0
                chut.pulse = 0
                if mode != "girl":
                    girl.nipple_presses = 0
                    girl.clit_presses = 0
                    girl.boob_size = 70
                    girl.nipple_color = NIPPLE_PINK
                    girl.milk_active = False
                    girl.hole_open = 0
                    girl.orgasming = False

    for p in particles[:]:
        p.update()
        if p.life <= 0:
            particles.remove(p)

    screen.fill(BG)

    if mode == "boobs":
        title = font.render("Boobs pe click kar... doodh nikalega", True, TEXT)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 30))
        left_boob.update(mouse_pos, mouse_pressed)
        right_boob.update(mouse_pos, mouse_pressed)
        left_boob.draw(screen)
        right_boob.draw(screen)
        btn_text = "Change to Lund"
        hint = small_font.render("Boobs pe click/hold karo", True, (160, 110, 130))

    elif mode == "dick":
        title = font.render("Balls 5x = Kala Bada Lund | 6x = Zor ka Favara", True, TEXT)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 30))
        dick.update(mouse_pos, mouse_pressed)
        dick.draw(screen)
        btn_text = "Change to Chut"
        hint = small_font.render("Testicles 5 baar dabao → kala 12 inch | 6 baar → strong cum", True, (160, 110, 130))

    elif mode == "chut":
        title = font.render("Clit pe dabao... pani + aah sound", True, TEXT)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 30))
        chut.update(mouse_pos, mouse_pressed)
        chut.draw(screen)
        btn_text = "Change to Nude Ladki"
        hint = small_font.render("Clit pe click/hold karo", True, (160, 110, 130))

    else:
        title = font.render("Nude Ladki - Nipples & Clit dabao", True, TEXT)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 30))
        girl.update(mouse_pos, mouse_pressed)
        girl.draw(screen)
        btn_text = "Back to Boobs"
        hint = small_font.render("Nipple 5x = size+color | 6x = doodh | Clit 5x = orgasm", True, (160, 110, 130))

    for p in particles:
        p.draw(screen)

    draw_button(screen, btn_text, hover_button)
    screen.blit(hint, (WIDTH//2 - hint.get_width()//2, HEIGHT - 115))

    pygame.display.flip()

pygame.quit()