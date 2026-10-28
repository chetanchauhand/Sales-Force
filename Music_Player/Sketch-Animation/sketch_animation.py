
import cv2
import pygame
import numpy as np
import os
import sys

# Window setup
pygame.init()

W, H = 900, 750
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Realistic Pencil Sketch Animation")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)
title_font = pygame.font.SysFont("Arial", 28, bold=True)

# Exact project folder path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Photo filename
photo_path = os.path.join(BASE_DIR, "name.jpeg")

# Check whether the photo exists
if not os.path.isfile(photo_path):
    print("ERROR: Photo not found!")
    print("Expected photo location:")
    print(photo_path)
    print("Please keep name.jpeg inside the Sketch-Animation folder.")
    pygame.quit()
    sys.exit()

# Load photo
photo = cv2.imread(photo_path)

if photo is None:
    print("ERROR: Photo could not be opened.")
    print("Check that the file is a valid JPEG image.")
    pygame.quit()
    sys.exit()

print("Photo loaded successfully!")

# Resize while maintaining aspect ratio
h, w = photo.shape[:2]
scale = min(820 / w, 590 / h)

nw = int(w * scale)
nh = int(h * scale)

photo = cv2.resize(
    photo,
    (nw, nh),
    interpolation=cv2.INTER_AREA
)

# Convert photo into pencil sketch
gray = cv2.cvtColor(photo, cv2.COLOR_BGR2GRAY)
inverted = 255 - gray

blurred = cv2.GaussianBlur(
    inverted, (21, 21), 0
)

inverted_blur = 255 - blurred

sketch = cv2.divide(
    gray,
    inverted_blur,
    scale=256.0
)

# Improve contrast
sketch = cv2.normalize(
    sketch, None, 0, 255, cv2.NORM_MINMAX
)

sketch = sketch.astype(np.uint8)

# Convert sketch to Pygame surface
rgb = cv2.cvtColor(sketch, cv2.COLOR_GRAY2RGB)

surface = pygame.surfarray.make_surface(
    np.transpose(rgb, (1, 0, 2))
)

# Paper background and image position
paper = (249, 247, 239)

x = (W - nw) // 2
y = 85 + (590 - nh) // 2

# Animation controls
progress = 0
speed = 4
paused = False
running = True

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                running = False

            elif event.key == pygame.K_SPACE:
                paused = not paused

            elif event.key == pygame.K_r:
                progress = 0
                paused = False

            elif event.key == pygame.K_UP:
                speed = min(20, speed + 1)

            elif event.key == pygame.K_DOWN:
                speed = max(1, speed - 1)

    # Background
    screen.fill(paper)

    # Heading
    heading = title_font.render(
        "PENCIL ART", True, (45, 42, 38)
    )

    screen.blit(
        heading,
        (W // 2 - heading.get_width() // 2, 20)
    )

    # Reveal sketch from top to bottom
    visible = min(progress, nh)

    if visible > 0:
        crop = pygame.Rect(0, 0, nw, visible)
        screen.blit(surface, (x, y), crop)

    # Update animation
    if not paused and progress < nh:
        progress = min(progress + speed, nh)

    # Progress bar
    bar_x, bar_y = 220, 680
    bar_w, bar_h = 460, 8

    pygame.draw.rect(
        screen,
        (220, 215, 205),
        (bar_x, bar_y, bar_w, bar_h),
        border_radius=4
    )

    fill_w = int(bar_w * progress / nh)

    if fill_w > 0:
        pygame.draw.rect(
            screen,
            (80, 75, 68),
            (bar_x, bar_y, fill_w, bar_h),
            border_radius=4
        )

    # Status message
    if progress >= nh:
        status = "Sketch complete! Press R to replay"
    elif paused:
        status = "Paused | SPACE to continue"
    else:
        status = "Drawing... SPACE: Pause | UP/DOWN: Speed"

    label = font.render(
        status, True, (60, 55, 50)
    )

    screen.blit(
        label,
        (W // 2 - label.get_width() // 2, 710)
    )

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
