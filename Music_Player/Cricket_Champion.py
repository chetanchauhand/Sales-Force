import pygame
import random

pygame.init()

W, H = 900, 600
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Cricket Champions")
clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas", 25)
big = pygame.font.SysFont("consolas", 40)

runs, wickets, balls = 0, 0, 0
choice = None
message = "Press SPACE to play a shot"
game_over = False
ball_pos = [450, 250]
batting = True

def draw_text(text, x, y, color=(255, 255, 255), f=font):
    screen.blit(f.render(text, True, color), (x, y))

running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            if event.key == pygame.K_r and game_over:
                runs, wickets, balls = 0, 0, 0
                game_over = False
                message = "New innings! Press SPACE"

            if event.key == pygame.K_SPACE and not game_over:
                shot = random.choice([0, 1, 2, 3, 4, 6, "W"])
                balls += 1

                if shot == "W":
                    wickets += 1
                    message = "OUT! Wicket lost!"
                else:
                    runs += shot
                    message = f"You scored {shot} run(s)!"

                if wickets >= 10 or balls >= 30:
                    game_over = True
                    message = "INNINGS OVER! Press R to restart"

    screen.fill((20, 90, 45))

    # Stadium stands
    pygame.draw.rect(screen, (65, 65, 90), (0, 0, W, 130))
    for x in range(0, W, 35):
        pygame.draw.circle(screen, (220, 180, 80), (x, 35), 4)

    # Cricket field and pitch
    pygame.draw.ellipse(screen, (50, 150, 70), (80, 120, 740, 450))
    pygame.draw.rect(screen, (190, 155, 105), (385, 180, 130, 300))
    pygame.draw.line(screen, (255, 255, 255), (385, 220), (515, 220), 3)
    pygame.draw.line(screen, (255, 255, 255), (385, 440), (515, 440), 3)

    # Bowler
    pygame.draw.circle(screen, (255, 190, 140), (450, 160), 15)
    pygame.draw.line(screen, (30, 50, 200), (450, 175), (450, 215), 12)

    # Batsman
    pygame.draw.circle(screen, (255, 190, 140), (450, 390), 16)
    pygame.draw.line(screen, (30, 50, 200), (450, 407), (450, 455), 13)
    pygame.draw.line(screen, (230, 210, 170), (460, 420), (485, 390), 7)

    # Ball
    pygame.draw.circle(screen, (210, 35, 35), ball_pos, 8)

    draw_text("CRICKET CHAMPIONS", 20, 15, (255, 230, 50), big)
    draw_text(f"Runs: {runs}   Wickets: {wickets}/10", 20, 65)
    draw_text(f"Overs: {balls // 6}.{balls % 6}", 20, 100)
    draw_text(message, 170, 525, (255, 255, 100))
    draw_text("SPACE: Shot | R: Restart | ESC: Exit", 180, 565)

    pygame.display.flip()

pygame.quit()