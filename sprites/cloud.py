import pygame
import random

class Cloud(pygame.sprite.Sprite):
    # static so only set once
    IMAGE = None

    def __init__(self, game_state):
        super().__init__()
        self.game_state = game_state
        self.game_state.all_sprites.add(self)

        # init static var if not already
        if Cloud.IMAGE is None:
            image = pygame.image.load(
                "./assets/images/cloud1.png"
            ).convert_alpha()
            image.set_alpha(128)

            Cloud.IMAGE = pygame.transform.scale(
                image, 
                (190, 135)
            )
        

        # pos and velocity
        self.x = random.randint(-950, -190)
        self.y = random.randint(0, 300)

        self.speed = 1

        # draw
        self.surf = Cloud.IMAGE
        self.rect = self.surf.get_rect(center=(self.x, self.y))
    
    def update(self):
        self.x += self.speed
        self.rect = self.surf.get_rect(center=(self.x, self.y))
