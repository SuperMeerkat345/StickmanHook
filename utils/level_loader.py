import json

from sprites.platform import Platform
from sprites.bounce_pad import BouncePad
from sprites.swing import Swing
from sprites.player import Player

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
        self.game_state.all_sprites.add(self.game_state.player)

        # INIT CAMERA
        #self.camera = 


        for obj in level["objects"]:
            obj_type = obj["type"]

            if obj_type == "swing":
                swing = Swing(
                    self.game_state,
                    obj["x"],
                    obj["y"]
                )
                self.game_state.all_sprites.add(swing)
                self.game_state.swings.add(swing)

            elif obj_type == "platform":
                platform = Platform(
                    self.game_state,
                    obj["x"],
                    obj["y"],
                    obj["width"],
                    obj["height"],
                    obj["rotation"]
                )

                self.game_state.all_sprites.add(platform)
                self.game_state.platforms.add(platform)

            elif obj_type == "bounce_pad":
                bounce_pad = BouncePad(
                    self.game_state,
                    obj["x"],
                    obj["y"],
                    obj["width"],
                    obj["height"],
                    obj["rotation"]
                )

                self.game_state.all_sprites.add(bounce_pad)
                self.game_state.platforms.add(bounce_pad)
        
    #def unload(self)