import pygame
import math
import random

pygame.init()

WIDTH, HEIGHT = 900, 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lusty Animation - Boobs to Lund 🔥")

clock = pygame.time.Clock()
FPS = 60

# Colors
BG = (18, 8, 12)
SKIN = (255, 210, 180)
NIPPLE = (220, 90, 90)
DARK_NIPPLE = (180, 50, 50)
MILK = (255, 255, 240)
DICK = (255, 200, 170)
BALL = (240, 190, 160)
CUM = (255, 255, 230)
BUTTON = (180, 50, 80)
BUTTON_HOVER = (220, 70, 100)
TEXT = (255, 180, 200)

font = pygame.font.SysFont("Arial", 26, bold=True)
small_font = pygame.font.SysFont("Arial", 18)

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
        self.size = random.randint(3, 7)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.25  # gravity
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
            # Milk spray
            for _ in range(4):
                angle = random.uniform(-0.8, 0.8)
                speed = random.uniform(4, 9)
                particles.append(Particle(
                    self.x + random.uniform(-10, 10),
                    self.y + self.offset_y + self.radius * 0.3,
                    MILK,
                    (math.sin(angle) * speed, -math.cos(angle) * speed - 2),
                    life=50
                ))

        self.vel_y += 0.55
        self.offset_y += self.vel_y
        self.vel_y *= 0.91
        self.vel_y -= self.offset_y * 0.09
        self.jiggle *= 0.9
        if self.jiggle < 0.4:
            self.jiggle = random.uniform(0.6, 1.8)

        self.radius = self.base_radius + math.sin(pygame.time.get_ticks() * 0.005 + self.x) * 2.5 + self.jiggle * 0.5

    def draw(self, surface):
        pygame.draw.circle(surface, SKIN, (int(self.x), int(self.y + self.offset_y)), int(self.radius))
        pygame.draw.circle(surface, (255, 230, 200),
                           (int(self.x - self.radius*0.22), int(self.y + self.offset_y - self.radius*0.28)),
                           int(self.radius * 0.32))
        nipple_y = self.y + self.offset_y + self.radius * 0.22
        pygame.draw.circle(surface, NIPPLE, (int(self.x), int(nipple_y)), int(self.radius * 0.17))
        pygame.draw.circle(surface, DARK_NIPPLE, (int(self.x), int(nipple_y)), int(self.radius * 0.08))

# ==================== LUND + BALLS ====================
class Dick:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2 + 40
        self.shaft_length = 180
        self.shaft_width = 48
        self.ball_radius = 42
        self.stroke = 0          # 0 to 1 (up down)
        self.stroking = False
        self.stroke_speed = 0
        self.cumming = False
        self.cum_timer = 0
        self.ball_press = 0

    def update(self, mouse_pos, mouse_pressed):
        mx, my = mouse_pos
        # Balls area check
        left_ball_x = self.x - 45
        right_ball_x = self.x + 45
        ball_y = self.y + 30

        dist_left = math.hypot(mx - left_ball_x, my - ball_y)
        dist_right = math.hypot(mx - right_ball_x, my - ball_y)

        if (dist_left < self.ball_radius + 15 or dist_right < self.ball_radius + 15) and mouse_pressed:
            self.ball_press = 12
            if not self.stroking and not self.cumming:
                self.stroking = True
                self.stroke_speed = 0.08

        self.ball_press = max(0, self.ball_press - 0.6)

        if self.stroking:
            self.stroke += self.stroke_speed
            if self.stroke >= 1:
                self.stroke = 1
                self.stroke_speed = -0.09
            elif self.stroke <= 0:
                self.stroke = 0
                self.stroke_speed = 0.08
                # Chance to cum after some strokes
                if random.random() < 0.25:
                    self.stroking = False
                    self.cumming = True
                    self.cum_timer = 90

        if self.cumming:
            self.cum_timer -= 1
            if self.cum_timer > 40:
                # Cum particles
                for _ in range(3):
                    particles.append(Particle(
                        self.x + random.uniform(-8, 8),
                        self.y - self.shaft_length + 20,
                        CUM,
                        (random.uniform(-2.5, 2.5), random.uniform(-11, -5)),
                        life=70
                    ))
            if self.cum_timer <= 0:
                self.cumming = False

    def draw(self, surface):
        # Balls
        ball_y = self.y + 30
        press_offset = self.ball_press * 0.8
        pygame.draw.circle(surface, BALL, (self.x - 45, int(ball_y + press_offset)), self.ball_radius)
        pygame.draw.circle(surface, BALL, (self.x + 45, int(ball_y + press_offset)), self.ball_radius)
        # Ball highlight
        pygame.draw.circle(surface, (255, 220, 190), (self.x - 55, int(ball_y - 10 + press_offset)), 14)
        pygame.draw.circle(surface, (255, 220, 190), (self.x + 35, int(ball_y - 10 + press_offset)), 14)

        # Shaft
        current_length = self.shaft_length * (0.85 + 0.15 * abs(math.sin(self.stroke * math.pi)))
        if self.cumming:
            current_length = self.shaft_length * 1.05

        shaft_top = self.y - current_length
        pygame.draw.rect(surface, DICK, 
                         (self.x - self.shaft_width//2, shaft_top, self.shaft_width, current_length),
                         border_radius=20)
        # Head
        pygame.draw.circle(surface, (255, 180, 150), (self.x, int(shaft_top + 10)), self.shaft_width//2 + 4)
        pygame.draw.circle(surface, (240, 140, 120), (self.x, int(shaft_top + 10)), self.shaft_width//2 - 6)

        # Veins simple
        pygame.draw.line(surface, (220, 160, 140), 
                         (self.x - 8, shaft_top + 40), 
                         (self.x - 5, self.y - 20), 3)

# ==================== BUTTON ====================
button_rect = pygame.Rect(WIDTH//2 - 100, HEIGHT - 70, 200, 48)

def draw_button(surface, text, hover):
    color = BUTTON_HOVER if hover else BUTTON
    pygame.draw.rect(surface, color, button_rect, border_radius=12)
    pygame.draw.rect(surface, (255, 120, 150), button_rect, 2, border_radius=12)
    txt = font.render(text, True, (255, 255, 255))
    surface.blit(txt, (button_rect.centerx - txt.get_width()//2, button_rect.centery - txt.get_height()//2))

# ==================== MAIN ====================
left_boob = Boob(WIDTH//2 - 130, HEIGHT//2 - 40, 115)
right_boob = Boob(WIDTH//2 + 130, HEIGHT//2 - 40, 115)
dick = Dick()

mode = "boobs"   # "boobs" or "dick"

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
                mode = "dick" if mode == "boobs" else "boobs"
                particles.clear()
                dick.stroking = False
                dick.cumming = False
                dick.stroke = 0

    # Update particles
    for p in particles[:]:
        p.update()
        if p.life <= 0:
            particles.remove(p)

    screen.fill(BG)

    if mode == "boobs":
        title = font.render("Boobs pe click kar... doodh nikalega 🥛", True, TEXT)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 30))
        left_boob.update(mouse_pos, mouse_pressed)
        right_boob.update(mouse_pos, mouse_pressed)
        left_boob.draw(screen)
        right_boob.draw(screen)
        # cleavage
        pygame.draw.line(screen, (200, 160, 140), (WIDTH//2-12, HEIGHT//2-50), (WIDTH//2+12, HEIGHT//2-50), 3)
        btn_text = "Change to Lund"
    else:
        title = font.render("Balls dabao... masturbate hoga 💦", True, TEXT)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 30))
        dick.update(mouse_pos, mouse_pressed)
        dick.draw(screen)
        btn_text = "Back to Boobs"

    # Draw particles
    for p in particles:
        p.draw(screen)

    draw_button(screen, btn_text, hover_button)

    # Hint
    if mode == "boobs":
        hint = small_font.render("Boobs pe click/hold karo doodh ke liye", True, (160, 110, 130))
    else:
        hint = small_font.render("Testicles (balls) pe click karke hold karo", True, (160, 110, 130))
    screen.blit(hint, (WIDTH//2 - hint.get_width()//2, HEIGHT - 110))

    pygame.display.flip()

pygame.quit()