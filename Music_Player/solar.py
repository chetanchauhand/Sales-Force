from vpython import *

scene = canvas(
    title="Interactive Solar System",
    width=1000,
    height=650,
    background=vector(0, 0, 0)
)
scene.caption = "Drag to rotate | Scroll to zoom"

sun = sphere(
    pos=vector(0, 0, 0),
    radius=1.2,
    color=color.orange,
    emissive=True
)

local_light(pos=vector(0, 0, 0), color=color.white)

planets = [
    {"name": "Mercury", "r": 0.18, "orbit": 2.0,
     "speed": 1.5, "color": color.gray(0.7)},
    {"name": "Venus", "r": 0.28, "orbit": 3.0,
     "speed": 1.1, "color": color.orange},
    {"name": "Earth", "r": 0.32, "orbit": 4.2,
     "speed": 0.8, "color": color.cyan},
    {"name": "Mars", "r": 0.24, "orbit": 5.4,
     "speed": 0.65, "color": color.red},
    {"name": "Jupiter", "r": 0.65, "orbit": 7.0,
     "speed": 0.4, "color": color.yellow},
    {"name": "Saturn", "r": 0.52, "orbit": 8.7,
     "speed": 0.3, "color": color.orange}
]

objects = []

for p in planets:
    ring(
        pos=vector(0, 0, 0),
        axis=vector(0, 1, 0),
        radius=p["orbit"],
        thickness=0.008,
        color=color.gray(0.3)
    )

    body = sphere(
        pos=vector(p["orbit"], 0, 0),
        radius=p["r"],
        color=p["color"],
        make_trail=(p["name"] == "Earth"),
        retain=150
    )

    label_obj = label(
        pos=body.pos,
        text=p["name"],
        height=12,
        box=False,
        opacity=0
    )

    if p["name"] == "Saturn":
        ring(
            pos=body.pos,
            axis=vector(0, 1, 0),
            radius=p["r"] * 1.7,
            thickness=0.09,
            color=color.gray(0.7)
        )

    objects.append((p, body, label_obj))

t = 0
while True:
    rate(60)
    t += 0.01

    for p, body, label_obj in objects:
        angle = t * p["speed"]

        body.pos = vector(
            p["orbit"] * cos(angle),
            0.15 * sin(angle * 2),
            p["orbit"] * sin(angle)
        )
        label_obj.pos = body.pos + vector(0, p["r"] + 0.2, 0)