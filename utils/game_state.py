import pygame
import utils.constants as constants

from utils.level_loader import LevelLoader
from ui.menu import Menu

class GameState:
    def __init__(self):
        # app
        self.virtual_screen = pygame.Surface((constants.VIRTUAL_WIDTH, constants.VIRTUAL_HEIGHT), pygame.SRCALPHA)
        self.displaysurface = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT), pygame.SCALED)
        self.menu = None

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
        self.cloud_manager = None

        # for re-spawning (starting position)
        self.start_pos = pygame.math.Vector2(0, 0)

        # load it in now
        self.level_loader = LevelLoader(self)
        self.level_loader.load("./scenes/levels/level_1.json")
    
