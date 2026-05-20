import pygame
import utils.constants as constants
from enum import Enum

currentsong = ""
enumLength = 3
currentNum = 0

class music(Enum):
    TIMEFORADVENTURE = "./assets/audio/time_for_adventure.mp3"
    STORY5MEETING = "./assets/audio/Story5meeting.mp3"
    SMELLSLIKETEENSPIRIT = "./assets/audio/SmellsLikeTeamSpirit.mp3"


def drawPause(surface, font):
    pygame.mixer.music.pause()
    pygame.draw.rect(surface, (128, 128, 128, 150), [0,0,constants.VIRTUAL_WIDTH, constants.VIRTUAL_HEIGHT])
    surface.blit(font.render('PAUSE', True, 'red'), (constants.WIDTH/2-15, 160))
    leftArrow = pygame.draw.polygon(surface, (255, 255, 255), [((constants.WIDTH/2-20-200),constants.HEIGHT/2), ((constants.WIDTH/2-200),constants.HEIGHT/2-20), ((constants.WIDTH/2-200),constants.HEIGHT/2+20)])
    rightArrow = pygame.draw.polygon(surface, (255, 255, 255), [((constants.WIDTH/2+20+200),constants.HEIGHT/2), ((constants.WIDTH/2+200),constants.HEIGHT/2+20), ((constants.WIDTH/2+200),constants.HEIGHT/2-20)])
    song = pygame.draw.rect(surface, (128,128,128), [(constants.WIDTH/2-190), (constants.HEIGHT/2-20), (380), (40),])
    surface.blit(font.render(currentsong, True, 'red'), ((constants.WIDTH/2-180), (constants.HEIGHT/2-12)))
    return surface, leftArrow, rightArrow, song

def goRight(num):
    if num < enumLength-1:
        num += 1
    else: 
        num = 0
    print(num)
    return num

def goLeft(num):
    if num < enumLength and num > 0:
        num -= 1
    else: 
        num = enumLength-1
    print(num)
    return num

def play(filename, start = 0, repeat = -1):
  
    pygame.mixer.init(frequency=16000)
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play(repeat, start)
    # while pygame.mixer.music.get_busy() == True:
    #     continue


def queue(filename):
    pygame.mixer.music.queue(filename)

