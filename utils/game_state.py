import pygame
import utils.constants as constants

class GameState:
    def __init__(self):
        # app
        self.virtual_screen = pygame.Surface((constants.VIRTUAL_WIDTH, constants.VIRTUAL_HEIGHT), pygame.SRCALPHA)
        self.displaysurface = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT), pygame.SCALED)

        # groups
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.swings = pygame.sprite.Group()

        # global flags
        self.paused = False


        self.game_won = False
        # global level attributes 
        # start with none, they get init'd when the level loader loads a level
        self.player = None
        self.camera = None
        self.finish_line = None

        # for re-spawning (starting position)
        self.start_pos = pygame.math.Vector2(0, 0)
    
