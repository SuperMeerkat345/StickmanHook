import pygame
import math

class BouncePad(pygame.sprite.Sprite):
    def __init__(self, game_state, x, y, w, h, rot):
        super().__init__()
        game_state.all_sprites.add(self)
        game_state.platforms.add(self)

        # store real geometry
        self.pos = pygame.math.Vector2(x, y)
        self.width = w
        self.height = h
        self.angle = rot

        # visual
        base = pygame.Surface((w, h), pygame.SRCALPHA)
        base.fill((125, 125, 0))
        self.surf = pygame.transform.rotate(base, -rot)
        self.rect = self.surf.get_rect(center=(x, y))

    def update(self):
        pass