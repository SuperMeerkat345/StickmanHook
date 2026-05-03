import pygame

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.surf = pygame.Surface((w, h))
        self.surf.fill((0, 0, 0))
        self.rect = self.surf.get_rect(topleft=(x, y))

    def update(self):
        pass