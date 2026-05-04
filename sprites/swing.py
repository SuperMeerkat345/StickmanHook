import pygame

class Swing(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.pos = pygame.math.Vector2(x, y)
        self.radius = 15
        self.diameter = self.radius*2
        
        # visual
        self.surf = pygame.Surface((self.diameter, self.diameter), pygame.SRCALPHA)
        self.color = (0, 255, 0)
        
        pygame.draw.circle(self.surf, self.color, (self.radius, self.radius), self.radius)
        self.rect = self.surf.get_rect(center=(self.pos.x, self.pos.y))

    def update(self):
        pass