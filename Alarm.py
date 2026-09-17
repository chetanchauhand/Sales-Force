# Alarm Clock
import time
from datetime import datetime

alarm = input("Enter alarm time (HH:MM): ")

print("Alarm set...")

while True:
    current_time = datetime.now().strftime("%H:%M")

    if current_time == alarm:
        print(" ALARM! Wake Up! ")
        break

    time.sleep(1)