import pygame

def play(filename):
  
    pygame.mixer.init(frequency=16000)
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play(0, 1)
    # while pygame.mixer.music.get_busy() == True:
    #     continue


def queue(filename):
    pygame.mixer.music.queue(filename)