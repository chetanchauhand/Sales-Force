import tkinter as tk
from time import strftime

root = tk.Tk()
root.title("Digital Clock")
root.geometry("400x200")

def update_time():
    current_time = strftime("%H:%M:%S")
    label.config(text=current_time)
    label.after(1000, update_time)

label = tk.Label(root, font=("Arial", 40))
label.pack(pady=50)

update_time()
root.mainloop()