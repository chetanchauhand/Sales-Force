
from ursina import *
import random

app = Ursina()
window.title = "NEON RACING 3D"
window.color = color.black

Sky(color=color.rgb(3, 4, 22))

road = Entity(
    model="cube", color=color.rgb(18, 18, 38),
    scale=(12, 0.2, 100), position=(0, -0.2, 20)
)

for x in [-6, 6]:
    Entity(model="cube", color=color.cyan,
           scale=(0.08, 0.08, 100),
           position=(x, -0.05, 20))

lanes = []
for z in range(-20, 65, 8):
    for x in [-2, 2]:
        lanes.append(Entity(
            model="cube", color=color.azure,
            scale=(0.07, 0.04, 3),
            position=(x, -0.04, z)
        ))

car = Entity(
    model="cube", color=color.cyan,
    scale=(1.2, 0.6, 2),
    position=(0, 0.5, -8)
)

Entity(model="cube", color=color.rgb(40, 60, 100),
       scale=(0.8, 0.3, 0.8),
       parent=car, position=(0, 0.65, 0))

obstacles = []
for i in range(6):
    obstacle = Entity(
        model="cube",
        color=color.rgb(255, 0, 150),
        scale=(1.3, 1, 1.5),
        position=(random.choice([-4, 0, 4]),
                  0.5, i * 12 + 12)
    )
    obstacles.append(obstacle)

camera.position = (0, 7, -19)
camera.rotation_x = 15

score = 0
game_over = False

score_text = Text(
    text="SCORE: 0",
    position=(-0.85, 0.45),
    scale=1.5, color=color.cyan
)

message = Text(
    text="",
    origin=(0, 0), scale=2,
    background=True
)

def update():
    global score, game_over

    if game_over:
        return

    dt = time.dt

    if held_keys["a"] or held_keys["left arrow"]:
        car.x -= 6 * dt
    if held_keys["d"] or held_keys["right arrow"]:
        car.x += 6 * dt

    car.x = max(-5, min(5, car.x))

    for lane in lanes:
        lane.z -= 18 * dt
        if lane.z < -15:
            lane.z += 80

    for obstacle in obstacles:
        obstacle.z -= 18 * dt

        if obstacle.z < -13:
            obstacle.z = random.uniform(45, 70)
            obstacle.x = random.choice([-4, 0, 4])
            score += 10
            score_text.text = f"SCORE: {score}"

        if (abs(obstacle.x - car.x) < 1.1
                and abs(obstacle.z - car.z) < 1.5):
            game_over = True
            message.text = (
                f"GAME OVER\nSCORE: {score}\n"
                "Close window to exit"
            )

app.run()
