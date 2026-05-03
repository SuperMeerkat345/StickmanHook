import pygame
import math

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, rot):
        super().__init__()
        # store real geometry
        self.pos = pygame.math.Vector2(x, y)
        self.width = w
        self.height = h
        self.angle = rot

        # visual
        base = pygame.Surface((w, h), pygame.SRCALPHA)
        base.fill((0, 0, 0))
        self.surf = pygame.transform.rotate(base, -rot)
        self.rect = self.surf.get_rect(center=(x, y))

    def update(self):
        pass