import json

from sprites.platform import Platform
from sprites.bounce_pad import BouncePad
from sprites.swing import Swing

class LevelLoader:
    def __init__(self, all_sprites, platforms, swings):
        # groups
        self.all_sprites = all_sprites
        self.platforms = platforms
        self.swings = swings

    def load(self, path):
        try:
            with open(path, 'r') as level_file:
                level = json.load(level_file)
        except FileNotFoundError:
            print("The file was not found.")
        except json.JSONDecodeError:
            print("Failed to decode JSON. Check the file format.")

        for obj in level["objects"]:
            obj_type = obj["type"]

            if obj_type == "swing":
                swing = Swing(
                    obj["x"],
                    obj["y"]
                )
                self.all_sprites.add(swing)
                self.swings.add(swing)

            elif obj_type == "platform":
                platform = Platform(
                    obj["x"],
                    obj["y"],
                    obj["width"],
                    obj["height"],
                    obj["rotation"]
                )

                self.all_sprites.add(platform)
                self.platforms.add(platform)

            elif obj_type == "bounce_pad":
                bounce_pad = BouncePad(
                    obj["x"],
                    obj["y"],
                    obj["width"],
                    obj["height"],
                    obj["rotation"]
                )

                self.all_sprites.add(bounce_pad)
                self.platforms.add(bounce_pad)
        
    #def unload(self)