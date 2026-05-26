import json
import pygame

# utils
import utils.constants as constants
from utils.camera import Camera

from sprites.platform import Platform
from sprites.bounce_pad import BouncePad
from sprites.swing import Swing
from sprites.player import Player
from sprites.finish_line import FinishLine

class LevelLoader:
    def __init__(self, game_state):
        self.game_state = game_state

    def load(self, path):
        try:
            with open(path, 'r') as level_file:
                level = json.load(level_file)
        except FileNotFoundError:
            print("The file was not found.")
        except json.JSONDecodeError:
            print("Failed to decode JSON. Check the file format.")

        # INIT PLAYER
        self.game_state.player = Player(
            self.game_state, # world reference 
            level["player_spawn"]["x"], # set x & y positions
            level["player_spawn"]["y"]
        )

        # init starting/respawn point
        self.game_state.start_pos = pygame.math.Vector2(level["player_spawn"]["x"], level["player_spawn"]["y"])

        # INIT CAMERA
        self.game_state.camera = Camera(constants.VIRTUAL_WIDTH, constants.VIRTUAL_HEIGHT)

        # finish line
        self.game_state.finish_line = FinishLine(self.game_state, level["finish_line_pos"])

        for obj in level["objects"]:
            obj_type = obj["type"]

            if obj_type == "swing":
                swing = Swing(
                    self.game_state,
                    obj["x"],
                    obj["y"]
                )
            
            elif obj_type == "platform":
                platform = Platform(
                    self.game_state,
                    obj["x"],
                    obj["y"],
                    obj["width"],
                    obj["height"],
                    obj["rotation"]
                )

            elif obj_type == "bounce_pad":
                bounce_pad = BouncePad(
                    self.game_state,
                    obj["x"],
                    obj["y"],
                    obj["width"],
                    obj["height"],
                    obj["rotation"]
                )

        
    #def unload(self)