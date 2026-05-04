import pygame
import math
import utils.constants as constants
from sprites.platform import Platform
from sprites.bounce_pad import BouncePad

class Player(pygame.sprite.Sprite):
    def __init__(self, all_sprites, platforms, swings):
        super().__init__()
        
        # visual
        self.radius = 15
        self.diameter = self.radius*2
        self.surf = pygame.Surface((self.diameter, self.diameter), pygame.SRCALPHA)
        pygame.draw.circle(self.surf, (255, 0, 0), (self.radius, self.radius), self.radius)
        self.rect = self.surf.get_rect()

        # physics
        self.pos = pygame.math.Vector2(10, 10)
        self.vel = pygame.math.Vector2(0, 0)
        self.acc = pygame.math.Vector2(0, 0)
        
        # world reference (auto-updated)
        self.all_sprites = all_sprites
        self.platforms = platforms
        self.swings = swings
    
    def update(self):
        self.acc = pygame.math.Vector2(0, constants.GRAVITY) # zero acceleration at start of frame

        self.process_input() # check which keys are held to determine acceleration        
        self.move() # move based on new acceleration
        self.step() # step through the velocity vector for the frame in order to prevent collision
        
        # zero velocity if going too slow
        if abs(self.vel.x) < 0.05:
            self.vel.x = 0
        if abs(self.vel.y) < 0.05:
            self.vel.y = 0
        
        
        self.rect.center = self.pos # sync physics body and rendered 
        

    def move(self):
        # account for friction
        #self.acc.x += self.vel.x * -constants.FRICTION

        # update velocity and position vectors
        self.vel += self.acc
        #self.pos += self.vel + 0.5 * self.acc # physics engine trick

    def step(self):
        # designed to scale amount of steps checked per frame with velocity
        steps = int(self.vel.length() // self.radius) + 1
        steps = max(1, min(steps, constants.MAX_STEPS))  # clamp

        step_vel = self.vel / steps

        for _ in range(steps):
            step_vel = self.vel / steps
            self.pos += step_vel # step forward
            self.resolve_collisions()

        
    # you have no clue how much work went into ts
    # hardest physics problem ive ever done...
    def resolve_collisions(self):
        for platform in self.platforms:
            # step 0: rotate system to regular x,y plane
            dist = self.pos - platform.pos
            theta = platform.angle # degrees

            # relative player position in new coordinate system
            relative = dist.rotate(-theta) # negative angle since we are going backwards

            # step 1: find closest pt on rectangle
            closest_x = max(-platform.width/2, min(relative.x, platform.width/2)) # rect at (0, 0), player pos stored in relative vector
            closest_y = max(-platform.height/2, min(relative.y, platform.height/2))

            # step 2: check if collision
            dx = relative.x - closest_x
            dy = relative.y - closest_y
            
            # if the point is outisde the circle, no collision
            # else, collision and we need to fix
            if dx*dx + dy*dy >= self.radius*self.radius:
                continue

            # step 3: get normal line of reflection surface
            normal_local = pygame.math.Vector2(dx, dy)

            if normal_local.length() == 0: # exact center, just pick whichever side is closest
                if abs(relative.x) > abs(relative.y):
                    normal_local = pygame.math.Vector2(1 if relative.x > 0 else -1, 0)
                else:
                    normal_local = pygame.math.Vector2(0, 1 if relative.y > 0 else -1)
            else:
                normal_local = normal_local.normalize()

            
            # step 4: calculate new velocity
            # https://math.stackexchange.com/questions/13261/how-to-get-a-reflection-vector
            normal = normal_local.rotate(theta)

            
            if isinstance(platform, BouncePad):
                self.vel = self.vel.reflect(normal) * 1.1
            elif isinstance(platform, Platform):
                self.vel = self.vel.reflect(normal) * 0.8
            

            # step 5: resolve penetration
            distance = pygame.math.Vector2(dx, dy).length()
            penetration = self.radius - distance
            self.pos += normal * penetration * 1.01

            #break # exit after first collision, we aint fancy around here
    
    def process_input(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.acc.x -= constants.ACCEL
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.acc.x += constants.ACCEL

    

