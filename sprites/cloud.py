import pygame
import random

import utils.constants as constants

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
        player_pos = self.game_state.player.pos
        self.x = random.randint( # set bounds around the players position
            int(player_pos.x-constants.VIRTUAL_WIDTH),
            int(player_pos.x-constants.VIRTUAL_WIDTH/1.5)
        )
        self.y = random.randint(0, 300)
        self.speed = random.random()*2 # 0-2

        # when to kill cloud
        self.death_barrier = random.randint( # set bounds around the players position
            int(player_pos.x+constants.VIRTUAL_WIDTH/1.5),
            int(player_pos.x+constants.VIRTUAL_WIDTH)
        )

        # draw
        self.surf = Cloud.IMAGE.copy()
        self.rect = self.surf.get_rect(center=(self.x, self.y))
    
    def update(self):
        self.x += self.speed
        self.rect = self.surf.get_rect(center=(self.x, self.y)) # update pos

        if self.x > self.death_barrier:
            self.kill_transition()

    def kill_transition(self):
        if self.surf.get_alpha() == 0:
            cloud = Cloud(self.game_state) # create new cloud before killing this one
            self.kill()                    # to satisfy conservation of clouds law
        else:
            self.surf.set_alpha(self.surf.get_alpha()-1)