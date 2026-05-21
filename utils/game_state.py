import pygame

class GameState:
    def __init__(self):
        # Groups
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.swings = pygame.sprite.Group()

        # global flags
        self.paused = False

        # global level attributes 
        # start with none, they get init'd when the level loader loads a level
        self.player = None
        self.camera = None

        # for re-spawning
        self.startx = 0
        self.starty = 0
    
