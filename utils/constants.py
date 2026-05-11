import tkinter as tk

root = tk.Tk()
# Get width and height in pixels
WIDTH = root.winfo_screenwidth()
HEIGHT = root.winfo_screenheight()

VIRTUAL_WIDTH, VIRTUAL_HEIGHT = 1920, 1080

# Window size
# WIDTH = 1000
# HEIGHT = 1000

print(f"Screen Size: {WIDTH} x {HEIGHT} pixels")
root.destroy()
# Window settings
FPS = 60

# Physics
FRICTION = 0.12
GRAVITY = 0.5
ACCEL = 0.5 # horizontal acceleartion of player
MAX_STEPS = 50 # maximum amount of steps for a collision
MIN_BOUNCE_SPEED = 5 # minimum bounce from bounce pad
