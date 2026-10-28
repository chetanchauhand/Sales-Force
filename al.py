
import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
import threading
import winsound
import time

# ---------------- CONFIGURATION ----------------

BG = "#0B1020"
PANEL = "#151D32"
ACCENT = "#E6B25E"
TEXT = "#F3F5FA"
MUTED = "#9AA8C2"
RED = "#FF5364"
GREEN = "#46D6A0"

root = tk.Tk()
root.title("NOVA | Smart Alarm")
root.geometry("520x690")
root.resizable(False, False)
root.configure(bg=BG)

alarm_time = None
alarm_enabled = False
ringing = False
snoozing = False
stop_sound = threading.Event()
blink_state = False

# ---------------- SOUND ENGINE ----------------

def sound_engine():
    while not stop_sound.is_set():
        try:
            # Three alternating tones
            for frequency in (1000, 1400, 1000):
                if stop_sound.is_set():
                    break
                winsound.Beep(frequency, 350)
                if stop_sound.wait(0.08):
                    break
        except RuntimeError:
            break

def start_ringing():
    global ringing

    if ringing:
        return

    ringing = True
    stop_sound.clear()

    threading.Thread(
        target=sound_engine,
        daemon=True
    ).start()

    update_ring_animation()

def stop_ringing():
    global ringing
    ringing = False
    stop_sound.set()
    status_label.config(
        text="ALARM STOPPED",
        fg=GREEN
    )
    ring_button_frame.pack_forget()

def update_ring_animation():
    global blink_state

    if not ringing:
        return

    blink_state = not blink_state

    root.configure(
        bg=RED if blink_state else BG
    )

    status_label.config(
        text="WAKE UP!  ALARM RINGING",
        fg=RED if blink_state else ACCENT
    )

    root.after(400, update_ring_animation)

# ---------------- CLOCK ----------------

def update_clock():
    now = datetime.now()

    clock_label.config(
        text=now.strftime("%I:%M:%S %p")
    )

    date_label.config(
        text=now.strftime("%A, %d %B %Y")
    )

    if alarm_enabled and alarm_time:
        if now >= alarm_time:
            trigger_alarm()

    root.after(250, update_clock)

# ---------------- ALARM CONTROLS ----------------

def set_alarm():
    global alarm_time, alarm_enabled, snoozing

    value = time_entry.get().strip()

    try:
        parsed = datetime.strptime(value, "%H:%M")
    except ValueError:
        messagebox.showerror(
            "Invalid Time",
            "Enter time in 24-hour format, e.g. 06:30 or 18:45."
        )
        return

    now = datetime.now()

    alarm_time = now.replace(
        hour=parsed.hour,
        minute=parsed.minute,
        second=0,
        microsecond=0
    )

    if alarm_time <= now:
        alarm_time += timedelta(days=1)

    alarm_enabled = True
    snoozing = False

    alarm_info.config(
        text="NEXT ALARM  •  " +
        alarm_time.strftime("%d %b, %I:%M %p"),
        fg=ACCENT
    )

    status_label.config(
        text="ALARM ARMED",
        fg=GREEN
    )

def disable_alarm():
    global alarm_enabled, alarm_time, snoozing

    alarm_enabled = False
    alarm_time = None
    snoozing = False

    if ringing:
        stop_ringing()

    root.configure(bg=BG)

    alarm_info.config(
        text="NO ALARM SET",
        fg=MUTED
    )

    status_label.config(
        text="ALARM DISABLED",
        fg=MUTED
    )

def trigger_alarm():
    global alarm_enabled

    alarm_enabled = False

    ring_button_frame.pack(
        pady=15
    )

    start_ringing()

def snooze_alarm():
    global alarm_time, alarm_enabled, snoozing

    stop_ringing()
    root.configure(bg=BG)

    alarm_time = datetime.now() + timedelta(minutes=5)
    alarm_enabled = True
    snoozing = True

    alarm_info.config(
        text="SNOOZED UNTIL  " +
        alarm_time.strftime("%I:%M %p"),
        fg=ACCENT
    )

    status_label.config(
        text="5-MINUTE SNOOZE ACTIVE",
        fg=GREEN
    )

    ring_button_frame.pack_forget()

# ---------------- UI HELPERS ----------------

def make_button(parent, text, command, color, fg=BG):
    return tk.Button(
        parent,
        text=text,
        command=command,
        bg=color,
        fg=fg,
        activebackground=TEXT,
        activeforeground=BG,
        font=("Segoe UI", 11, "bold"),
        relief="flat",
        cursor="hand2",
        padx=14,
        pady=12,
        bd=0
    )

# ---------------- HEADER ----------------

tk.Label(
    root,
    text="N O V A",
    font=("Segoe UI", 13, "bold"),
    fg=ACCENT,
    bg=BG
).pack(pady=(22, 2))

tk.Label(
    root,
    text="SMART ALARM CLOCK",
    font=("Segoe UI", 10),
    fg=MUTED,
    bg=BG
).pack()

# ---------------- CLOCK PANEL ----------------

clock_panel = tk.Frame(
    root,
    bg=PANEL,
    padx=20,
    pady=22
)
clock_panel.pack(
    fill="x",
    padx=24,
    pady=22
)

clock_label = tk.Label(
    clock_panel,
    text="12:00:00 AM",
    font=("Segoe UI", 35, "bold"),
    fg=TEXT,
    bg=PANEL
)
clock_label.pack()

date_label = tk.Label(
    clock_panel,
    text="Loading date...",
    font=("Segoe UI", 11),
    fg=MUTED,
    bg=PANEL
)
date_label.pack(pady=(6, 0))

# ---------------- ALARM INPUT ----------------

tk.Label(
    root,
    text="SET YOUR WAKE-UP TIME",
    font=("Segoe UI", 10, "bold"),
    fg=MUTED,
    bg=BG
).pack(pady=(0, 10))

input_frame = tk.Frame(root, bg=BG)
input_frame.pack()

time_entry = tk.Entry(
    input_frame,
    font=("Segoe UI", 24, "bold"),
    width=9,
    justify="center",
    bg=PANEL,
    fg=TEXT,
    insertbackground=TEXT,
    relief="flat"
)
time_entry.insert(0, "06:30")
time_entry.pack(ipady=9, padx=5)

tk.Label(
    root,
    text="24-hour format  •  HH:MM",
    font=("Segoe UI", 9),
    fg=MUTED,
    bg=BG
).pack(pady=8)

# ---------------- ACTION BUTTONS ----------------

buttons = tk.Frame(root, bg=BG)
buttons.pack(pady=12)

make_button(
    buttons, "SET ALARM",
    set_alarm, ACCENT
).pack(side="left", padx=5)

make_button(
    buttons, "DISABLE",
    disable_alarm, PANEL, TEXT
).pack(side="left", padx=5)

# ---------------- STATUS ----------------

alarm_info = tk.Label(
    root,
    text="NO ALARM SET",
    font=("Segoe UI", 11, "bold"),
    fg=MUTED,
    bg=BG
)
alarm_info.pack(pady=(15, 8))

status_label = tk.Label(
    root,
    text="SYSTEM READY",
    font=("Segoe UI", 10, "bold"),
    fg=GREEN,
    bg=BG
)
status_label.pack(pady=5)

# ---------------- RINGING BUTTONS ----------------

ring_button_frame = tk.Frame(
    root,
    bg=BG
)

make_button(
    ring_button_frame,
    "SNOOZE 5 MIN",
    snooze_alarm,
    ACCENT
).pack(side="left", padx=5)

make_button(
    ring_button_frame,
    "STOP ALARM",
    stop_ringing,
    RED
).pack(side="left", padx=5)

ring_button_frame.pack_forget()

# ---------------- FOOTER ----------------

tk.Label(
    root,
    text="SPACE-TIME  •  YOUR DAY STARTS HERE",
    font=("Segoe UI", 8),
    fg=MUTED,
    bg=BG
).pack(side="bottom", pady=16)

def on_close():
    stop_sound.set()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)

update_clock()
root.mainloop()
