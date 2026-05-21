import pygame
import utils.constants as constants
from enum import Enum
import random

#music vars
currentsong = ""
enumLength = 6
currentNum = 0
startedMusic = True

#cloud vars
numclouds = 0
clouds = []

class music(Enum):
    TIMEFORADVENTURE = "./assets/audio/time_for_adventure.mp3"
    STORY5MEETING = "./assets/audio/Story5meeting.mp3"
    SMELLSLIKETEENSPIRIT = "./assets/audio/SmellsLikeTeamSpirit.mp3"
    HAVENTOWNTHEME = "./assets/audio/HavenTownTheme.mp3"
    GERUDOVALLEY = "./assets/audio/GerudoValley.mp3"
    HEDWIGSTHEME = "./assets/audio/HedwigsTheme.mp3"


def drawPause(surface, font):
    pygame.mixer.music.pause()
    pygame.draw.rect(surface, (128, 128, 128, 150), [0,0,constants.VIRTUAL_WIDTH, constants.VIRTUAL_HEIGHT])
    surface.blit(font.render('PAUSE', True, 'red'), (constants.WIDTH/2-15, 160))
    leftArrow = pygame.draw.polygon(surface, (255, 255, 255), [((constants.WIDTH/2-20-200),constants.HEIGHT/2), ((constants.WIDTH/2-200),constants.HEIGHT/2-20), ((constants.WIDTH/2-200),constants.HEIGHT/2+20)])
    rightArrow = pygame.draw.polygon(surface, (255, 255, 255), [((constants.WIDTH/2+20+200),constants.HEIGHT/2), ((constants.WIDTH/2+200),constants.HEIGHT/2+20), ((constants.WIDTH/2+200),constants.HEIGHT/2-20)])
    song = pygame.draw.rect(surface, (128,128,128), [(constants.WIDTH/2-190), (constants.HEIGHT/2-20), (380), (40),])
    surface.blit(font.render(currentsong, True, 'red'), ((constants.WIDTH/2-180), (constants.HEIGHT/2-12)))
    pygame.mixer.music.load(music[currentsong].value)
    return surface, leftArrow, rightArrow, song

def drawCloud(surface, max = 3, num = numclouds):
    if not constants.pause:
        if num < max:
            screen = pygame.Surface((190, 135), pygame.SRCALPHA)
            cloud = pygame.image.load("./assets/images/cloud1.png").convert_alpha()
            cloud.set_alpha(128)
            cloud = pygame.transform.scale(cloud, (190, 135))
            screen.blit(cloud, (0,0))
            randnum1 = random.randint(1, 5)
            randnum2 = random.randint(0, 540)
            clouds.append( [screen, -190*randnum1, 540-(randnum2)])
            num += 1
            #print(clouds)
        for index, cloud in enumerate(clouds):
            surface.blit(cloud[0], (cloud[1], cloud[2]))
            clouds[index] = [cloud[0], ((1)+cloud[1]), (cloud[2])]
            if clouds[index][1] > constants.VIRTUAL_WIDTH:
                clouds.pop(index)
                num -= 1
        return num
    else:
        for index, cloud in enumerate(clouds):
            surface.blit(cloud[0], (cloud[1], cloud[2]))
            clouds[index] = [cloud[0], ((0)+cloud[1]), (cloud[2])]
        return num
   
    
def goRight(num):
    if num < enumLength-1:
        num += 1
    else: 
        num = 0
    #print(num)
    return num

def goLeft(num):
    if num < enumLength and num > 0:
        num -= 1
    else: 
        num = enumLength-1
    #print(num)
    return num

def play(filename, start = 0, repeat = -1):
  
    pygame.mixer.init(frequency=16000)
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play(repeat, start)
    # while pygame.mixer.music.get_busy() == True:
    #     continue


def queue(filename):
    pygame.mixer.music.queue(filename)