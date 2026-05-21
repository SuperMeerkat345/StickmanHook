import pygame
import utils.constants as constants

class Connector(pygame.sprite.Sprite):
    def __init__(self, game_state, obj1, obj2):
        super().__init__()
        game_state.all_sprites.add(self)

        self.game_state = game_state

        self.surf = pygame.Surface((abs(obj1.pos.x-obj2.pos.x), abs(obj1.pos.y-obj2.pos.y)), pygame.SRCALPHA)
        self.rect = self.surf.get_rect()

        self.obj1 = obj1
        self.obj2 = obj2

    def update(self):
        pygame.draw.line(
            self.game_state.virtual_screen,
            (255,255,255),
            self.game_state.camera.apply_pos(self.obj1.pos),
            self.game_state.camera.apply_pos(self.obj2.pos),
            5
        )