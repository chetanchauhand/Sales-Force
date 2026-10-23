
from ursina import *
import pygame
import math
import random
import os
import tempfile
import struct
import wave

# Generate sound effects locally, no downloads required
pygame.mixer.pre_init(22050, -16, 1, 512)
pygame.init()
pygame.mixer.init()

def make_sound(filename, frequency, duration, kind="engine"):
    rate = 22050
    frames = int(rate * duration)

    with wave.open(filename, "w") as wav:
        wav.setparams((1, 2, rate, frames, "NONE", "not compressed"))
        data = bytearray()

        for i in range(frames):
            t = i / rate
            envelope = max(0, 1 - t / duration)

            if kind == "impact":
                envelope *= math.exp(-12 * t)
                f = frequency * (1 + 0.5 * math.sin(2 * math.pi * 18 * t))
            elif kind == "engine":
                f = frequency + 45 * math.sin(2 * math.pi * 9 * t)
            else:
                f = frequency

            sample = math.sin(2 * math.pi * f * t)

            if kind == "impact":
                sample = 0.7 * sample + 0.3 * random.uniform(-1, 1)

            value = int(10000 * envelope * sample)
            data.extend(struct.pack("<h", value))

        wav.writeframes(data)

tmp = tempfile.gettempdir()
engine_file = os.path.join(tmp, "car_engine.wav")
impact_file = os.path.join(tmp, "car_impact.wav")
coin_file = os.path.join(tmp, "car_coin.wav")

make_sound(engine_file, 95, 0.7, "engine")
make_sound(impact_file, 110, 0.5, "impact")
make_sound(coin_file, 880, 0.15, "coin")

engine_sound = pygame.mixer.Sound(engine_file)
impact_sound = pygame.mixer.Sound(impact_file)
coin_sound = pygame.mixer.Sound(coin_file)

engine_sound.set_volume(0.25)
impact_sound.set_volume(0.65)
coin_sound.set_volume(0.35)

engine_channel = engine_sound.play(-1)
engine_channel.pause()

# 3D game
app = Ursina()
window.title = "NEON RACER - Pach Pach Edition"
window.color = color.rgb(5, 5, 20)
window.fps_counter.enabled = True

Sky(color=color.rgb(5, 5, 22))

road = Entity(
    model="cube", color=color.rgb(20, 20, 36),
    scale=(12, 0.2, 100), position=(0, -0.2, 15)
)

for x in (-6, 6):
    Entity(model="cube", color=color.cyan,
           scale=(0.1, 0.08, 100), position=(x, 0, 15))

# Neon lane markings
lanes = []
for z in range(-30, 70, 8):
    for x in (-2, 2):
        lanes.append(Entity(
            model="cube", color=color.azure,
            scale=(0.08, 0.04, 3),
            position=(x, -0.06, z)
        ))

# Car body
car = Entity(position=(0, 0.45, -8))
Entity(
    parent=car, model="cube",
    color=color.rgb(0, 200, 255),
    scale=(1.4, 0.5, 2.3)
)
Entity(
    parent=car, model="cube",
    color=color.rgb(35, 45, 90),
    scale=(1.0, 0.45, 0.9),
    position=(0, 0.42, 0.15)
)

# Headlights
for x in (-0.48, 0.48):
    Entity(
        parent=car, model="cube", color=color.yellow,
        scale=(0.25, 0.12, 0.08),
        position=(x, 0.05, 1.17)
    )

# Wheels
for x in (-0.77, 0.77):
    for z in (-0.7, 0.7):
        Entity(
            parent=car, model="sphere",
            color=color.black,
            scale=(0.3, 0.22, 0.3),
            rotation_z=90, position=(x, -0.2, z)
        )

# Obstacles
obstacles = []
for i in range(8):
    obstacle = Entity(
        model="cube",
        color=color.rgb(255, 0, 130),
        scale=(1.3, 1.1, 1.4),
        position=(random.choice([-4, 0, 4]), 0.55, i * 12 + 12)
    )
    obstacles.append(obstacle)

score = 0
speed = 18
game_over = False

score_text = Text(
    text="SCORE: 0",
    position=(-0.86, 0.45),
    scale=1.5, color=color.cyan
)
help_text = Text(
    text="A/D or ARROWS: STEER | SPACE: SOUND",
    position=(-0.86, 0.39),
    scale=0.9, color=color.white
)
message = Text(
    text="", origin=(0, 0),
    scale=2, background=True
)

camera.position = (0, 7, -19)
camera.rotation_x = 15
camera.fov = 90

def update():
    global score, game_over, speed

    if game_over:
        return

    dt = time.dt

    if held_keys["a"] or held_keys["left arrow"]:
        car.x -= 6 * dt
    if held_keys["d"] or held_keys["right arrow"]:
        car.x += 6 * dt

    car.x = max(-5, min(5, car.x))

    # Road movement
    for lane in lanes:
        lane.z -= speed * dt
        if lane.z < -18:
            lane.z += 96

    # Engine sound: faster pitch as speed increases
    if engine_channel:
        engine_channel.unpause()
        engine_channel.set_volume(0.2)
        
    for obstacle in obstacles:
        obstacle.z -= speed * dt

        if obstacle.z < -14:
            obstacle.z = random.uniform(48, 75)
            obstacle.x = random.choice([-4, 0, 4])
            score += 10
            score_text.text = f"SCORE: {score}"
            coin_sound.play()

        if (abs(obstacle.x - car.x) < 1.25
                and abs(obstacle.z - car.z) < 1.7):
            game_over = True
            engine_channel.pause()
            impact_sound.play()
            message.text = (
                f"CRASH! DHAMM!\nSCORE: {score}\n"
                "Close window to exit"
            )

def input(key):
    if key == "space":
        if engine_channel and engine_channel.get_busy():
            engine_channel.pause()
        elif engine_channel:
            engine_channel.unpause()

app.run()
