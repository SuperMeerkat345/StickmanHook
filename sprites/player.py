import pygame
import utils.constants as constants
from sprites.platform import Platform
from sprites.bounce_pad import BouncePad

class Player(pygame.sprite.Sprite):
    def __init__(self, all_sprites, platforms, swings):
        super().__init__()
        
        # visual
        self.surf = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.circle(self.surf, (255, 0, 0), (15, 15), 15)
        self.rect = self.surf.get_rect()

        # physics
        self.pos = pygame.math.Vector2(10, 10)
        self.vel = pygame.math.Vector2(0, 0)
        self.acc = pygame.math.Vector2(0, 0)

        # world reference (auto-updated)
        self.all_sprites = all_sprites
        self.platforms = platforms
        self.swings = swings

        # temp 
        self.on_ground = False
    
    def update(self):
        self.acc = pygame.math.Vector2(0, constants.GRAVITY) # zero acceleration at start of frame

        self.process_input() # check which keys are held to determine acceleration        
        self.move() # move based on new acceleration
        self.resolve_collisions() # handle collisions

    def move(self):
        # account for friction
        self.acc.x += self.vel.x * -constants.FRICTION

        # update velocity and position vectors
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc # physics engine trick

        # sync rect and position
        self.rect.midbottom = self.pos
        
    # need to improve
    def resolve_collisions(self):
        collisions = pygame.sprite.spritecollide(self, self.platforms, False)
        if collisions:
            
            self.pos.y = collisions[0].rect.top + 1 # put on top of collision
            self.vel.y = 0 # stop
            
            self.on_ground = True # back on ground
            

            #collision = collisions[0]
            #if isinstance(collision, Platform):
            #    pass
            #elif isinstance(collision, BouncePad):

    
    def process_input(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.acc.x -= constants.ACCEL
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.acc.x += constants.ACCEL
        if keys[pygame.K_SPACE]:
            self.jump()

    # temp func for testing collisions
    def jump(self):
        # check if bro is standing before letting him jump
        # he aint jesus gng
        if self.on_ground:
            self.vel.y = -15
            self.on_ground = False # not on ground no more



