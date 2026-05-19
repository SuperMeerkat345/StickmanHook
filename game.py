# system modules
import pygame
import sys


# local imports
import utils.constants as constants
from utils.camera import Camera
from utils.level_loader import LevelLoader
import utils.audio as audio


from sprites.player import Player
from sprites.platform import Platform
from sprites.bounce_pad import BouncePad

from sprites.swing import Swing
from sprites.connector import Connector

pygame.init()
clock = pygame.time.Clock()

# setup window
pygame.display.set_caption("Game")

# Design resolution (internal game logic runs here)
virtual_screen = pygame.Surface((constants.VIRTUAL_WIDTH, constants.VIRTUAL_HEIGHT))
displaysurface = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT), pygame.SCALED)

#audio.play("./assets/audio/SmellsLikeTeamSpirit.mp3")
#audio.queue("./assets/audio/time_for_adventure.mp3")


## INIT CODE
# CAMERA
camera = Camera(constants.VIRTUAL_WIDTH, constants.VIRTUAL_HEIGHT)

# GROUPS
all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()
swings = pygame.sprite.Group()

level_loader = LevelLoader(all_sprites, platforms, swings)
level_loader.load("./scenes/levels/test_level.json")

# --- PLAYER ---
P1 = Player(all_sprites, platforms, swings)
P1.pos = pygame.math.Vector2(500, 100)
all_sprites.add(P1)

## ENDINIT

# game loop
while True:
    # handle events
    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            pygame.display.toggle_fullscreen()
            pygame.display.set_mode((constants.WIDTH/4, constants.HEIGHT/4))
        # close game log
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
    # background + ui
    virtual_screen.fill((0, 0, 255))
    font = pygame.font.SysFont("Arial", 20)  # Use None for default font
    text_surface = font.render(f"FPS: {str(round(clock.get_fps()))} Velocity: {P1.vel}", True, (255, 255, 255))

    # draw sprites and update sprites
    camera.update(P1) # follow player with cam

    # draw rope if needed
    if P1.connection:
        pygame.draw.line(
            virtual_screen,
            (255,255,255),
            camera.apply_pos(P1.pos),
            camera.apply_pos(P1.connection.pos),
            5
        )

    for entity in all_sprites:
        virtual_screen.blit(entity.surf, camera.apply(entity.rect))
        entity.update()
    
    
        
    

    #scale screen
    scaled_screen = pygame.transform.scale(virtual_screen, (constants.WIDTH, constants.HEIGHT))
    displaysurface.blit(scaled_screen, (0, 0))
    displaysurface.blit(text_surface, (70, 70))
    
    pygame.display.flip()
    # re-render display
    pygame.display.update()
    clock.tick(constants.FPS) # limit loop to 60 fps

   
