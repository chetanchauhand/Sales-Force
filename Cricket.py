
import math
import random
import requests

from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import DirectButton, DirectLabel
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import (
    AmbientLight, DirectionalLight, Vec3, Vec4,
    TextNode
)

# Optional live cricket API key:
# Get one from https://cricketdata.org/
CRICKET_API_KEY = ""

TEAMS = [
    "India", "Australia", "England", "Pakistan",
    "New Zealand", "South Africa", "Sri Lanka",
    "Bangladesh", "Afghanistan", "West Indies"
]

MODES = ["Quick Match", "League Match", "Tournament", "World Cup"]


class CricketGame(ShowBase):
    def __init__(self):
        super().__init__()

        self.disableMouse()
        self.setBackgroundColor(0.015, 0.025, 0.06, 1)
        self.camera.setPos(0, -65, 36)
        self.camera.lookAt(0, 0, 0)

        self.ui = []
        self.game_objects = []
        self.home_index = 0
        self.away_index = 1
        self.mode_index = 0

        self.score = 0
        self.wickets = 0
        self.balls = 0
        self.max_balls = 12
        self.target = None
        self.ball_active = False
        self.ball_time = 0
        self.ball_start = None
        self.ball_end = None
        self.ball_obj = None
        self.swing_used = False
        self.shot_type = "Ground"
        self.game_state = "menu"
        self.innings = 1
        self.notice = "Choose a match to begin."

        self.setup_lighting()
        self.build_stadium()
        self.show_main_menu()

        self.accept("escape", self.back_to_menu)
        self.accept("space", self.swing)
        self.accept("b", self.bowl)
        self.accept("arrow_left", self.aim_left)
        self.accept("arrow_right", self.aim_right)
        self.accept("1", self.ground_shot)
        self.accept("2", self.lofted_shot)

        self.aim = 0
        self.taskMgr.add(self.update_game, "update_game")

    # ---------- 3D SCENE ----------

    def model(self, path, parent, pos, scale, color):
        obj = self.loader.loadModel(path)
        obj.reparentTo(parent)
        obj.setPos(*pos)
        obj.setScale(*scale)
        obj.setColor(*color)
        self.game_objects.append(obj)
        return obj

    def setup_lighting(self):
        ambient = AmbientLight("ambient")
        ambient.setColor(Vec4(0.55, 0.58, 0.65, 1))
        self.render.setLight(
            self.render.attachNewNode(ambient)
        )

        sun = DirectionalLight("stadium_light")
        sun.setColor(Vec4(1, 0.92, 0.78, 1))
        light_node = self.render.attachNewNode(sun)
        light_node.setHpr(-35, -55, 0)
        self.render.setLight(light_node)

    def build_stadium(self):
        # Ground and pitch
        self.model(
            "models/box", self.render,
            (0, 0, -1), (55, 48, 1),
            (0.07, 0.30, 0.12, 1)
        )

        self.model(
            "models/box", self.render,
            (0, 0, 0.05), (4, 19, 0.08),
            (0.62, 0.48, 0.30, 1)
        )

        # Stadium seating around the ground
        for side in [-1, 1]:
            for row in range(8):
                z = 1.0 + row * 0.65
                y = side * (23 + row * 0.9)

                self.model(
                    "models/box", self.render,
                    (0, y, z),
                    (48 - row * 1.2, 0.65, 0.55),
                    (0.15 + row * 0.008,
                     0.12 + row * 0.004,
                     0.25 + row * 0.008, 1)
                )

        for side in [-1, 1]:
            for row in range(6):
                x = side * (27 + row * 0.7)

                self.model(
                    "models/box", self.render,
                    (x, 0, 1 + row * 0.65),
                    (0.65, 38 - row, 0.55),
                    (0.12, 0.16, 0.27, 1)
                )

        # Floodlight towers
        for x in [-32, 32]:
            for y in [-25, 25]:
                self.model(
                    "models/box", self.render,
                    (x, y, 10), (0.35, 0.35, 10),
                    (0.65, 0.68, 0.72, 1)
                )

                self.model(
                    "models/box", self.render,
                    (x, y, 20), (2.2, 0.5, 0.6),
                    (1.0, 0.93, 0.72, 1)
                )

        # Pitch markings
        for y in [-8, 8]:
            self.model(
                "models/box", self.render,
                (0, y, 0.16), (3.8, 0.08, 0.025),
                (1, 1, 1, 1)
            )

        # Stumps at each end
        for y in [-8.5, 8.5]:
            for x in [-0.22, 0, 0.22]:
                self.model(
                    "models/box", self.render,
                    (x, y, 0.65), (0.055, 0.055, 0.65),
                    (1, 0.88, 0.55, 1)
                )

        # Simple 3D player silhouettes
        self.batter = self.make_player(0, -5.5, (0.12, 0.22, 0.72, 1))
        self.bowler = self.make_player(0, 6.0, (0.85, 0.15, 0.12, 1))

        # Fielders
        self.fielders = []
        for x, y in [
            (-13, -8), (13, -8), (-18, 0), (18, 0),
            (-12, 10), (12, 10), (-23, 14), (23, 14)
        ]:
            self.fielders.append(
                self.make_player(x, y, (0.85, 0.15, 0.12, 1))
            )

        self.ball_obj = self.model(
            "models/misc/sphere", self.render,
            (0, 6, 1), (0.19, 0.19, 0.19),
            (0.85, 0.04, 0.04, 1)
        )

        self.ball_obj.hide()

    def make_player(self, x, y, color):
        root = self.render.attachNewNode("player")
        root.setPos(x, y, 0)
        self.game_objects.append(root)

        self.model(
            "models/misc/sphere", root,
            (0, 0, 1.65), (0.42, 0.32, 0.65), color
        )
        self.model(
            "models/misc/sphere", root,
            (0, 0, 2.48), (0.28, 0.28, 0.28),
            (0.75, 0.55, 0.38, 1)
        )

        self.model(
            "models/box", root,
            (-0.17, 0, 0.55), (0.12, 0.15, 0.55),
            (0.9, 0.9, 0.92, 1)
        )
        self.model(
            "models/box", root,
            (0.17, 0, 0.55), (0.12, 0.15, 0.55),
            (0.9, 0.9, 0.92, 1)
        )

        return root

    # ---------- UI HELPERS ----------

    def clear_ui(self):
        for item in self.ui:
            item.destroy()
        self.ui.clear()

    def button(self, text, x, z, command, scale=0.055):
        item = DirectButton(
            text=text,
            scale=scale,
            pos=(x, 0, z),
            command=command,
            frameColor=(0.05, 0.25, 0.20, 0.96),
            text_fg=(1, 1, 1, 1),
            relief=1,
            borderWidth=(0.015, 0.015)
        )
        self.ui.append(item)
        return item

    def label(self, text, z, scale=0.075):
        item = DirectLabel(
            text=text,
            scale=scale,
            pos=(0, 0, z),
            frameColor=(0, 0, 0, 0),
            text_fg=(1, 0.88, 0.58, 1)
        )
        self.ui.append(item)
        return item

    # ---------- MENUS ----------

    def show_main_menu(self):
        self.game_state = "menu"
        self.clear_ui()
        self.label("CRICKET CHAMPIONS", 0.65, 0.105)
        self.label("3D CRICKET EXPERIENCE", 0.53, 0.045)

        self.button("PLAY", 0, 0.30, self.show_team_menu, 0.075)
        self.button("LIVE CRICKET SCORES (API)", 0, 0.12,
                    self.fetch_live_scores, 0.045)
        self.button("EXIT", 0, -0.08, self.userExit, 0.06)

        self.label(
            "SPACE: Swing   B: Bowl   LEFT/RIGHT: Aim",
            -0.48, 0.035
        )

    def show_team_menu(self):
        self.clear_ui()
        self.label("MATCH SETUP", 0.72, 0.09)

        self.home_label = self.label("", 0.43, 0.055)
        self.away_label = self.label("", 0.22, 0.055)
        self.mode_label = self.label("", 0.01, 0.055)

        self.button("CHANGE HOME TEAM", -0.42, 0.32,
                    self.change_home, 0.04)
        self.button("CHANGE OPPONENT", 0.42, 0.11,
                    self.change_away, 0.04)
        self.button("CHANGE MODE", 0, -0.12,
                    self.change_mode, 0.045)

        self.button("START MATCH", 0.38, -0.42,
                    self.start_match, 0.055)
        self.button("BACK", -0.38, -0.42,
                    self.show_main_menu, 0.055)

        self.refresh_setup()

    def refresh_setup(self):
        self.home_label["text"] = "YOUR TEAM: " + TEAMS[self.home_index]
        self.away_label["text"] = "OPPONENT: " + TEAMS[self.away_index]
        self.mode_label["text"] = "MODE: " + MODES[self.mode_index]

    def change_home(self):
        self.home_index = (self.home_index + 1) % len(TEAMS)
        if self.home_index == self.away_index:
            self.home_index = (self.home_index + 1) % len(TEAMS)
        self.refresh_setup()

    def change_away(self):
        self.away_index = (self.away_index + 1) % len(TEAMS)
        if self.away_index == self.home_index:
            self.away_index = (self.away_index + 1) % len(TEAMS)
        self.refresh_setup()

    def change_mode(self):
        self.mode_index = (self.mode_index + 1) % len(MODES)
        self.refresh_setup()

    # ---------- MATCH ----------

    def start_match(self):
        self.clear_ui()
        self.game_state = "playing"
        self.score = 0
        self.wickets = 0
        self.balls = 0
        self.innings = 1
        self.target = None
        self.max_balls = 12  # 2-over demo match
        self.aim = 0
        self.ball_active = False
        self.ball_obj.hide()

        self.score_label = OnscreenText(
            text="", pos=(-1.25, 0.88), scale=0.055,
            align=TextNode.ALeft,
            fg=(1, 1, 1, 1),
            mayChange=True
        )

        self.hint_label = OnscreenText(
            text="", pos=(0, -0.88), scale=0.05,
            align=TextNode.ACenter,
            fg=(1, 0.9, 0.55, 1),
            mayChange=True
        )

        self.ui.extend([self.score_label, self.hint_label])
        self.update_scoreboard()
        self.hint_label.setText(
            "Press B to bowl. When batting, press SPACE to hit. "
            "1 = Ground shot, 2 = Lofted shot."
        )

    def update_scoreboard(self):
        team = TEAMS[self.home_index] if self.innings == 1 else TEAMS[self.away_index]
        overs = f"{self.balls // 6}.{self.balls % 6}"
        target_text = f" | Target {self.target}" if self.target else ""
        self.score_label.setText(
            f"{team}  {self.score}/{self.wickets}   "
            f"Overs: {overs}{target_text}   "
            f"| {MODES[self.mode_index]}"
        )

    def bowl(self):
        if self.game_state != "playing" or self.ball_active:
            return
        if self.balls >= self.max_balls or self.wickets >= 3:
            self.end_innings()
            return

        self.ball_active = True
        self.ball_time = 0
        self.swing_used = False
        self.ball_start = Vec3(0, 6, 1.2)
        self.ball_end = Vec3(self.aim, -5.5, 0.65)
        self.ball_obj.setPos(self.ball_start)
        self.ball_obj.show()
        self.hint_label.setText("Ball coming! Time your shot with SPACE.")

    def swing(self):
        if self.game_state != "playing" or not self.ball_active:
            return
        if self.swing_used:
            return

        self.swing_used = True

        # A timing-based simplified cricket shot
        timing = abs(self.ball_time - 0.75)
        if timing < 0.18:
            result = random.choices(
                [0, 1, 2, 3, 4, 6, "W"],
                weights=[5, 12, 12, 5, 25, 25, 5]
            )[0]
        elif timing < 0.38:
            result = random.choice([0, 1, 1, 2, 3, 4, "W"])
        else:
            result = random.choice([0, 0, 1, "W"])

        self.complete_ball(result)

    def complete_ball(self, result):
        self.ball_active = False
        self.ball_obj.hide()
        self.balls += 1

        if result == "W":
            self.wickets += 1
            self.hint_label.setText("OUT! The fielding team takes a wicket.")
        else:
            self.score += result
            if result == 4:
                self.hint_label.setText("FOUR! Great boundary shot!")
            elif result == 6:
                self.hint_label.setText("SIX! The ball clears the boundary!")
            elif result == 0:
                self.hint_label.setText("Dot ball!")
            else:
                self.hint_label.setText(f"{result} run(s)!")

        # Simple fielding movement toward the hit direction
        for fielder in self.fielders:
            old_pos = fielder.getPos()
            fielder.setPos(
                old_pos.x + random.uniform(-0.6, 0.6),
                old_pos.y + random.uniform(-0.6, 0.6),
                old_pos.z
            )

        self.update_scoreboard()

        if self.target and self.score >= self.target:
            self.finish_match()
        elif self.balls >= self.max_balls or self.wickets >= 3:
            self.end_innings()

    def end_innings(self):
        if self.innings == 1:
            self.target = self.score + 1
            self.innings = 2
            self.score = 0
            self.wickets = 0
            self.balls = 0
            self.ball_active = False
            self.ball_obj.hide()
            self.hint_label.setText(
                f"Innings break! Target: {self.target}. "
                "Now play the chase."
            )
            self.update_scoreboard()
        else:
            self.finish_match()

    def finish_match(self):
        self.game_state = "finished"
        self.ball_active = False
        self.ball_obj.hide()
        self.clear_ui()

        if self.target and self.score >= self.target:
            result = TEAMS[self.away_index] + " wins the chase!"
        else:
            result = "Match completed!"

        self.label("MATCH FINISHED", 0.52, 0.095)
        self.label(result, 0.30, 0.06)
        self.label(
            f"Final score: {self.score}/{self.wickets}",
            0.12, 0.055
        )
        self.button("PLAY AGAIN", 0, -0.12, self.show_team_menu, 0.055)
        self.button("MAIN MENU", 0, -0.32, self.show_main_menu, 0.055)

    def ground_shot(self):
        self.shot_type = "Ground"
        if self.game_state == "playing":
            self.hint_label.setText("Ground shot selected. Press SPACE to hit.")

    def lofted_shot(self):
        self.shot_type = "Lofted"
        if self.game_state == "playing":
            self.hint_label.setText("Lofted shot selected. Press SPACE to hit.")

    def aim_left(self):
        self.aim = max(-2, self.aim - 0.4)

    def aim_right(self):
        self.aim = min(2, self.aim + 0.4)

    def update_game(self, task):
        dt = globalClock.getDt()

        if self.ball_active:
            self.ball_time += dt
            t = min(self.ball_time / 1.2, 1.0)

            pos = self.ball_start * (1 - t) + self.ball_end * t
            pos.z += math.sin(t * math.pi) * 2.5
            self.ball_obj.setPos(pos)

            if self.ball_time >= 1.2 and not self.swing_used:
                self.complete_ball(0)

        return task.cont

    # ---------- LIVE CRICKET API ----------

    def fetch_live_scores(self):
        if not CRICKET_API_KEY:
            self.notice = (
                "Get an API key from cricketdata.org, then set "
                "CRICKET_API_KEY at the top of this file."
            )
            print(self.notice)
            webbrowser_open("https://cricketdata.org/")
            return

        try:
            response = requests.get(
                "https://api.cricapi.com/v1/currentMatches",
                params={
                    "apikey": CRICKET_API_KEY,
                    "offset": 0
                },
                timeout=10
            )
            response.raise_for_status()
            data = response.json()

            print("\n--- LIVE CRICKET MATCHES ---")
            for match in data.get("data", [])[:10]:
                print(
                    match.get("name", "Match"),
                    "| Status:", match.get("status", "Unknown")
                )

            print("\nFull API response status:", data.get("status"))
            print("Check terminal for the latest results.")

        except Exception as error:
            print("Live API error:", error)

    def back_to_menu(self):
        if self.game_state in ("playing", "finished"):
            self.show_main_menu()


def webbrowser_open(url):
    import webbrowser
    webbrowser.open(url)


game = CricketGame()
game.run()
