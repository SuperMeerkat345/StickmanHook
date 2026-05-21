# deprecated

import pygame
import utils.constants as constants

class Connector(pygame.sprite.Sprite):
    def __init__(self, game_state, obj1, obj2):
        super().__init__()
        game_state.all_sprites.add(self)

        self.surf = virtual_screen
        self.rect = self.surf.get_rect()

        self.obj1 = obj1
        self.obj2 = obj2

    def update(self):
        self.surf.fill((255, 255, 255, 1)) # clear

        pygame.draw.line(
            self.surf, # surf
            (255, 255, 255), # color
            (self.obj1.pos.x, self.obj1.pos.y), # start
            (self.obj2.pos.x, self.obj2.pos.y), # end
            5 # width
        )