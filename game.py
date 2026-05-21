# system modules
import pygame
import sys


# local imports
import utils.constants as constants
from utils.camera import Camera
from utils.level_loader import LevelLoader
from utils.game_state import GameState
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
game_state = GameState()

# Load and scale the background image
background_image = pygame.image.load("./assets/images/background1.png").convert()
background_image = pygame.transform.scale(background_image, (constants.VIRTUAL_WIDTH, constants.VIRTUAL_HEIGHT))

audio.play(audio.music.HAVENTOWNTHEME.value)
audio.currentsong = audio.music.HAVENTOWNTHEME.name



## INIT CODE


level_loader = LevelLoader(game_state)
level_loader.load("./scenes/levels/test_level.json")

## ENDINIT

# game loop
while True:
    # handle events
    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            pygame.display.toggle_fullscreen()
            pygame.display.set_mode((constants.WIDTH/4, constants.HEIGHT/4))
        if keys[pygame.K_ESCAPE]:
            game_state.paused = not game_state.paused
        # close game log
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and game_state.paused:
            if leftArrow.collidepoint(event.pos):
                audio.currentNum = audio.goLeft(audio.currentNum)
                audio.currentsong = list(audio.music)[audio.currentNum].name
            if rightArrow.collidepoint(event.pos):
                audio.currentNum = audio.goRight(audio.currentNum)
                audio.currentsong = list(audio.music)[audio.currentNum].name

    # background + ui
    game_state.virtual_screen.fill((0, 0, 255))
    game_state.virtual_screen.blit(background_image, (0, 0))
    audio.numclouds = audio.drawCloud(game_state.virtual_screen, 3, audio.numclouds)
    font = pygame.font.SysFont("Arial", 20)  # Use None for default font
    text_surface = font.render(f"FPS: {str(round(clock.get_fps()))} Velocity: {game_state.player.vel}", True, (255, 255, 255))

    # draw sprites and update sprites
    game_state.camera.update(game_state.player) # follow player with cam

  

    for entity in game_state.all_sprites:
        game_state.virtual_screen.blit(entity.surf, game_state.camera.apply(entity.rect))
        if not game_state.paused:
            entity.update()
        
    

    #scale screen
    scaled_screen = pygame.transform.scale(game_state.virtual_screen, (constants.WIDTH, constants.HEIGHT))
    game_state.displaysurface.blit(scaled_screen, (0, 0))
    game_state.displaysurface.blit(text_surface, (70, 70))

    if game_state.paused == True:
        screen, leftArrow, rightArrow, song = audio.drawPause(game_state.virtual_screen, font)
        displaysurface.blit(screen, (0,0))
        audio.startedMusic = False
    else:
        pygame.mixer.music.unpause()
    
    # Check if music is not playing, then start it
    if not audio.startedMusic:
        audio.play(audio.music[audio.currentsong].value)
        audio.startedMusic = True

    pygame.display.flip()
    # re-render display
    pygame.display.update()
    clock.tick(constants.FPS) # limit loop to 60 fps

   
