import pygame

info = pygame.display.Info()

# Get width and height in pixels
WIDTH = info.current_w
HEIGHT = info.current_h

VIRTUAL_WIDTH, VIRTUAL_HEIGHT = 1920, 1080

# Window size
# WIDTH = 1000
# HEIGHT = 1000

print(f"Screen Size: {WIDTH} x {HEIGHT} pixels")
# Window settings
FPS = 60

# Physics
FRICTION = 0.12 # currently unused
GRAVITY = 0.5
ACCEL = 0.5 # horizontal acceleartion of player
MAX_STEPS = 50 # maximum amount of steps for a collision
MIN_BOUNCE_SPEED = 5 # minimum bounce from bounce pad
REST_THRESHOLD = 2 # when to rest on platforms

BOUNCEPAD_BOUNCE_MULT = 1.1
PLATFORM_BOUNCE_MULT = 0.8

DEATH_BARRIER = 2000 # if y > DEATH_BARRIER -> kill_player()