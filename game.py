# system modules
import pygame
import sys

# local imports
import utils.constants as constants
from sprites.player import Player
from sprites.platform import Platform
from sprites.bounce_pad import BouncePad

pygame.init()
clock = pygame.time.Clock()

# setup window
displaysurface = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
pygame.display.set_caption("Game")

## INIT CODE
# GROUPS
all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()
swings = pygame.sprite.Group()

# --- BOUNDARIES (keep player inside) ---
floor = Platform(500, 950, 1000, 50, 0)
left_wall = Platform(0, 500, 50, 1000, 0)
right_wall = Platform(1000, 500, 50, 1000, 0)
ceiling = Platform(500, 0, 1000, 50, 0)

for p in [floor, left_wall, right_wall, ceiling]:
    all_sprites.add(p)
    platforms.add(p)

# --- MAIN FLOOR BOUNCE ---
main_bounce = BouncePad(500, 800, 400, 40, 0)
all_sprites.add(main_bounce)
platforms.add(main_bounce)

# --- LEFT RAMP ---
left_ramp = BouncePad(250, 650, 300, 40, 30)
all_sprites.add(left_ramp)
platforms.add(left_ramp)

# --- RIGHT RAMP ---
right_ramp = BouncePad(750, 650, 300, 40, -30)
all_sprites.add(right_ramp)
platforms.add(right_ramp)

# --- VERTICAL LAUNCHER ---
launcher = BouncePad(500, 500, 200, 40, 90)
all_sprites.add(launcher)
platforms.add(launcher)

# --- MID AIR PLATFORM ---
mid_platform = Platform(500, 350, 300, 30, 0)
all_sprites.add(mid_platform)
platforms.add(mid_platform)

# --- ANGLED TRICK SHOT ---
trick1 = BouncePad(200, 400, 200, 30, -45)
trick2 = BouncePad(800, 400, 200, 30, 45)

for p in [trick1, trick2]:
    all_sprites.add(p)
    platforms.add(p)

# --- PLAYER ---
P1 = Player(all_sprites, platforms, swings)
P1.pos = pygame.math.Vector2(500, 100)
all_sprites.add(P1)
## ENDINIT

# game loop
while True:
    # handle events
    for event in pygame.event.get():
        # close game logic
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
    # background + ui
    displaysurface.fill((0, 0, 255))
    font = pygame.font.SysFont("Arial", 20)  # Use None for default font
    text_surface = font.render(f"FPS: {str(round(clock.get_fps()))} Velocity: {P1.vel}", True, (255, 255, 255))
    displaysurface.blit(text_surface, (30, 30))

    # draw sprites and update sprites
    for entity in all_sprites:
        displaysurface.blit(entity.surf, entity.rect)
        entity.update()

    # re-render display
    pygame.display.update()
    clock.tick(constants.FPS) # limit loop to 60 fps

   
