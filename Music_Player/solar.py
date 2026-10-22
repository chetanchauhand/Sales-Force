
from vpython import *
import requests
import webbrowser
import threading
import math
import time

# ---------------- SCENE ----------------
scene = canvas(
    title="REALISTIC SOLAR SYSTEM EXPLORER",
    width=1200,
    height=720,
    background=vector(0.005, 0.005, 0.025)
)

scene.forward = vector(-1, -0.5, -1)
scene.range = 35
scene.caption = (
    "\nClick a planet to search NASA's image library."
    "\nUse the mouse to rotate and zoom."
)

# ---------------- NASA API ----------------
NASA_API = "https://images-api.nasa.gov/search"

planet_facts = {
    "Sun": "Our star. Its gravity holds the solar system together.",
    "Mercury": "The smallest planet and closest to the Sun.",
    "Venus": "A rocky planet with an extremely hot atmosphere.",
    "Earth": "Our home planet, with liquid water on its surface.",
    "Mars": "The red planet, with a thin atmosphere.",
    "Jupiter": "The largest planet, famous for its Great Red Spot.",
    "Saturn": "A gas giant famous for its extensive rings.",
    "Uranus": "An ice giant that rotates on a strongly tilted axis.",
    "Neptune": "A distant ice giant with very strong winds.",
}

info = label(
    pos=vector(0, 12, 0),
    text="WELCOME\nClick any planet!",
    height=15,
    box=True,
    color=color.white,
    opacity=0.15
)

# ---------------- STAR FIELD ----------------
import random

random.seed(12)

for _ in range(500):
    star_pos = vector(
        random.uniform(-100, 100),
        random.uniform(-65, 65),
        random.uniform(-100, 100)
    )
    sphere(
        pos=star_pos,
        radius=random.uniform(0.04, 0.12),
        color=vector(0.7, 0.75, 1),
        emissive=True
    )

# ---------------- SUN ----------------
sun = sphere(
    pos=vector(0, 0, 0),
    radius=2.3,
    color=color.orange,
    emissive=True,
    shininess=0
)
sun.glow = sphere(
    pos=vector(0, 0, 0),
    radius=2.8,
    color=vector(1, 0.35, 0.03),
    opacity=0.12,
    emissive=True
)
sun.name = "Sun"

# ---------------- PLANETS ----------------
planet_data = [
    ("Mercury", 4, 0.35, color.gray(0.6), 0.24),
    ("Venus",   6, 0.58, vector(0.9, 0.65, 0.3), 0.62),
    ("Earth",   9, 0.65, color.blue, 1.0),
    ("Mars",   12, 0.48, vector(0.9, 0.25, 0.12), 1.88),
    ("Jupiter",17, 1.35, vector(0.8, 0.55, 0.35), 11.86),
    ("Saturn", 22, 1.1, vector(0.85, 0.75, 0.5), 29.4),
    ("Uranus", 27, 0.85, vector(0.4, 0.8, 0.85), 84),
    ("Neptune",32, 0.82, vector(0.2, 0.35, 1), 165)
]

planets = []

for name, orbit, size, shade, period in planet_data:
    # Orbit path
    curve(
        pos=[
            vector(orbit * math.cos(a * 2 * pi / 180), 0,
                   orbit * math.sin(a * 2 * pi / 180))
            for a in range(0, 361, 3)
        ],
        color=vector(0.22, 0.24, 0.35),
        radius=0.018
    )

    obj = sphere(
        pos=vector(orbit, 0, 0),
        radius=size,
        color=shade,
        shininess=0.25
    )

    obj.name = name
    obj.orbit = orbit
    obj.period = period
    obj.angle = random.uniform(0, 2 * pi)
    obj.base_color = shade

    # Saturn rings
    if name == "Saturn":
        obj.rings = ring(
            pos=obj.pos,
            axis=vector(0.25, 1, 0),
            radius=size * 1.8,
            thickness=size * 0.42,
            color=vector(0.8, 0.7, 0.5),
            opacity=0.75
        )

    planets.append(obj)

# ---------------- EARTH MOON ----------------
earth = next(p for p in planets if p.name == "Earth")

moon = sphere(
    pos=earth.pos + vector(1.1, 0, 0),
    radius=0.17,
    color=color.white,
    shininess=0.2
)

moon_angle = 0

# ---------------- NASA API SEARCH ----------------
def search_nasa(planet_name):
    try:
        response = requests.get(
            NASA_API,
            params={
                "q": planet_name + " planet",
                "media_type": "image",
                "page_size": 10
            },
            timeout=12
        )
        response.raise_for_status()

        items = response.json().get("collection", {}).get("items", [])

        for item in items:
            data = item.get("data", [{}])[0]
            links = item.get("links", [])

            if links and data.get("title"):
                title = data.get("title", "NASA image")
                description = data.get("description", "")
                image_url = links[0].get("href", "")

                print("\nNASA IMAGE:", title)
                print("DESCRIPTION:", description[:500])
                print("IMAGE URL:", image_url)

                info.text = (
                    planet_name + "\n"
                    + planet_facts.get(planet_name, "") + "\n\n"
                    + "NASA result:\n" + title[:120]
                    + "\n\nImage link printed in terminal."
                )

                # Open the NASA image in your browser
                if image_url:
                    webbrowser.open(image_url)
                return

        info.text = (
            planet_name + "\n"
            + planet_facts.get(planet_name, "")
            + "\nNo NASA image result found."
        )

    except Exception as error:
        print("NASA API error:", error)
        info.text = (
            planet_name + "\n"
            + planet_facts.get(planet_name, "")
            + "\nNASA API unavailable. Check internet."
        )


def on_click(event):
    picked = event.pick

    if picked is None:
        return

    name = getattr(picked, "name", None)

    if name:
        info.text = (
            name + "\n"
            + planet_facts.get(name, "Solar system object")
            + "\nSearching NASA image library..."
        )
        threading.Thread(
            target=search_nasa,
            args=(name,),
            daemon=True
        ).start()


scene.bind("click", on_click)

# ---------------- ANIMATION ----------------
paused = False
speed = 1.0
last_time = time.time()

def toggle_pause(button):
    global paused
    paused = not paused
    button.text = "Resume" if paused else "Pause"

def change_speed(slider):
    global speed
    speed = slider.value

button(text="Pause", bind=toggle_pause)
scene.append_to_caption("   Animation speed: ")
slider(
    min=0.1,
    max=5,
    value=1,
    step=0.1,
    bind=change_speed
)
scene.append_to_caption("\n")

# ---------------- MAIN LOOP ----------------
while True:
    rate(60)

    now = time.time()
    dt = min(now - last_time, 0.1)
    last_time = now

    if paused:
        continue

    moon_angle += 0.8 * speed * dt

    for p in planets:
        # Illustrative orbital speeds, not to scale
        p.angle += (0.35 / math.sqrt(p.period)) * speed * dt * 10

        p.pos = vector(
            p.orbit * math.cos(p.angle),
            0,
            p.orbit * math.sin(p.angle)
        )

        if p.name == "Saturn":
            p.rings.pos = p.pos

    moon.pos = earth.pos + vector(
        1.1 * math.cos(moon_angle),
        0.15 * math.sin(moon_angle),
        1.1 * math.sin(moon_angle)
    )
