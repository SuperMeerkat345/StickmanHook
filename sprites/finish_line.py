import pygame

import utils.constants as constants

class FinishLine(pygame.sprite.Sprite):
    def __init__(self, game_state, x):
        super().__init__()

        self.origin_image = pygame.image.load("./assets/images/finishline1.png")
        self.image = self.origin_image.convert()

        self.game_state = game_state
        self.game_state.all_sprites.add(self)

        self.x = x

        # rendering
        self.surf = pygame.Surface((100, constants.VIRTUAL_HEIGHT), pygame.SRCALPHA)
        self.surf.fill((0, 255, 0, 150)) # includes transparency

        self.rect = self.surf.get_rect(center=(self.x, constants.VIRTUAL_HEIGHT/2))
        

    def update(self):
        pass
    
    def draw(self):
        self.surf.blit(self.image, (0, 0))