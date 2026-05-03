# system modules
import pygame
import sys

# local imports
import utils.constants as constants
from sprites.player import Player
from sprites.platform import Platform
from sprites.bounce_pad import BouncePad

pygame.init()

# setup window
displaysurface = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
pygame.display.set_caption("Game")

## INIT CODE
# GROUPS
all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()
swings = pygame.sprite.Group()


p1 = Platform(10, 400, 300, 50)
all_sprites.add(p1)
platforms.add(p1)

b1 = BouncePad(300, 300, 100, 20)
all_sprites.add(b1)
platforms.add(b1)

P1 = Player(all_sprites, platforms, swings)
all_sprites.add(P1)
## END

# game loop
while True:
    # handle events
    for event in pygame.event.get():
        # close game logic
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
    # background
    displaysurface.fill((0, 0, 255))

    # draw sprites and update sprites
    for entity in all_sprites:
        displaysurface.blit(entity.surf, entity.rect)
        entity.update()

    # re-render display
    pygame.display.update()
    pygame.time.Clock().tick(constants.FPS) # limit loop to 60 fps
