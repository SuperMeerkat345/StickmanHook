import pygame
import math
from time import sleep
import utils.constants as constants
from sprites.platform import Platform
from sprites.bounce_pad import BouncePad
from sprites.connector import Connector

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
        self.steps = 1 # number of simulations to run per frame
        
        # world reference (auto-updated)
        self.all_sprites = all_sprites
        self.platforms = platforms
        self.swings = swings

        # connection
        self.connection = None
    
    def update(self):
        # step 0: calculate accel
        self.acc = pygame.math.Vector2(0, constants.GRAVITY) # zero acceleration at start of frame
        self.process_input() # check which keys are held to determine acceleration (DEBUG)    
       
        # step 1: apply accel to velocity
        self.vel += self.acc

        # step 2: using the calculated velocity, step through the movements
        self.step() # step through the velocity vector for the frame in order to prevent collision

        # zero velocity if going too slow
        if abs(self.vel.x) < 0.05:
            self.vel.x = 0
        if abs(self.vel.y) < 0.3:
            self.vel.y = 0
        
        
        self.rect.center = self.pos # sync physics body and rendered 

    # steps through the velocities per frame
    def step(self):
        # designed to scale amount of steps checked per frame with velocity
        self.steps = int(self.vel.length() // self.radius) + 1
        self.steps = max(1, min(self.steps, constants.MAX_STEPS))  # clamp

        step_vel = self.vel / self.steps

        for _ in range(self.steps):
            if not self.connection:
                step_vel = self.vel / self.steps
                self.pos += step_vel # step forward
            else: # connected
                self.project_velocity()

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

                # set a minimum velocity to have after a bounce
                if self.vel.length() < constants.MIN_BOUNCE_SPEED:
                    self.vel = (self.vel / self.vel.length()) * constants.MIN_BOUNCE_SPEED
            elif isinstance(platform, Platform):
                self.vel = self.vel.reflect(normal) * 0.8

            # step 5: resolve penetration
            distance = pygame.math.Vector2(dx, dy).length()
            penetration = self.radius - distance
            self.pos += normal * penetration *1.01

            #break # exit after first collision, we aint fancy around here
    
    # connects to the nearest swing
    def connect(self):
        # if alr connected or no swings, exit
        if self.connection or len(self.swings) == 0:
            return
        

        # get swing with the lowest distance to the player
        closest_swing = min(
            self.swings, 
            key=lambda swing: math.dist((self.pos.x, self.pos.y), (swing.pos.x, swing.pos.y))
        )
        
        self.connection = Connector(self, closest_swing) # make the connection
        self.all_sprites.add(self.connection) # add it to the world environment

        # --- LOCK THE LENGTH HERE ---
        self.active_rope_length = (self.pos - closest_swing.pos).length() *0.9
        
        self.all_sprites.add(self.connection)
    
    def project_velocity(self):
        if self.connection is None:
            return
        
        anchor_pos = self.connection.obj2.pos
        radius_vector = self.pos - anchor_pos
        radius_length = radius_vector.length()

        # step 1: check if inside the anchor
        if radius_length == 0:
            return
        perpendicular_vector = radius_vector.rotate(90)
        self.vel = self.vel.project(perpendicular_vector) # psuedo velocity vector

        # step 2: move player towards the anchor
        #self.pos += radius_vector.rotate(180)

        # step 3: check direction of rotation
        direction = 1 if self.vel.dot(perpendicular_vector) > 0 else -1

        # step 4: snap position
        # s = r*theta (where theta in rad)
        theta = (self.vel.length() / self.steps) / radius_length
        theta = math.degrees(theta) * direction

        # anchor position summed with radius vector which is clamped to the constant rope length
        self.pos = anchor_pos + (radius_vector.normalize()*self.active_rope_length).rotate(theta)
        



    # processes key inputs
    def process_input(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.acc.x -= constants.ACCEL
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.acc.x += constants.ACCEL
        if keys[pygame.K_SPACE]:
            self.connect()
        elif self.connection: # if not pressing space, clear connection
            self.all_sprites.remove(self.connection)
            self.connection = None

    

    

