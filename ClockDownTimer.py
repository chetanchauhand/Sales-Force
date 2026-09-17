# ClockDown Timer.

import time

seconds = int(input("Enter seconds: "))

while seconds > 0:
    minutes = seconds //60
    sec = seconds % 60
    
    print(f"{minutes:02d}:{sec:02d}")
    
    time.sleep(1)

    seconds -= 1

print("Time's Up!")