import pygame
import math
import time
import utils.constants as constants
import utils.audio as audio
from sprites.platform import Platform
from sprites.bounce_pad import BouncePad
from sprites.connector import Connector
from utils.camera import Camera

class Player(pygame.sprite.Sprite):
    def __init__(self, game_state, startx, starty):
        super().__init__()
        # auto-add to groups
        game_state.all_sprites.add(self)
        
        
        # visual
        self.radius = 15
        self.diameter = self.radius*2
        self.surf = pygame.Surface((self.diameter, self.diameter), pygame.SRCALPHA)
        pygame.draw.circle(self.surf, (255, 0, 0), (self.radius, self.radius), self.radius)
        self.rect = self.surf.get_rect()

        # self.skin = pygame.image.load("./assets/images/player1.png").convert_alpha()
        # self.skin.set_alpha(128)
        # self.skin = pygame.transform.scale(self.skin, (59.79, 135))
        # self.surf = pygame.transform.scale(self.surf, (59.79, 135))

        # physics
        self.pos = pygame.math.Vector2(startx, starty)
        self.vel = pygame.math.Vector2(0, 0)
        self.acc = pygame.math.Vector2(0, 0)
        self.steps = 1 # number of simulations to run per frame
        
        # world reference (auto-updated)
        self.game_state = game_state

        # connection
        self.connection = None
    
    def update(self):
        self.check_death()

        # step 0: calculate accel
        self.acc = pygame.math.Vector2(0, constants.GRAVITY) # zero acceleration at start of frame
        self.process_input() # check which keys are held to determine acceleration (DEBUG)    

        self.check_win()
       
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
        self.steps = int(self.vel.length() // self.radius) + 1
        self.steps = max(1, min(self.steps, constants.MAX_STEPS))

        for _ in range(self.steps):
            if self.connection:
                self.project_velocity() # arc
            else:
                self.pos += self.vel / self.steps # normal movement
            
            # always res
            self.resolve_collisions()
            
            # reconstrain
            if self.connection:
                anchor_pos = self.connection.obj2.pos
                diff = self.pos - anchor_pos
                if diff.length() > 0:
                    self.pos = anchor_pos + diff.normalize() * self.active_rope_length
        
        
    # you have no clue how much work went into ts
    # hardest physics problem ive ever done...
    def resolve_collisions(self):
        for platform in self.game_state.platforms:
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
                # add to velocity
                self.vel = self.vel.reflect(normal) * constants.BOUNCEPAD_BOUNCE_MULT

                # set a minimum velocity to have after a bounce
                if self.vel.length() < constants.MIN_BOUNCE_SPEED:
                    self.vel = (self.vel / self.vel.length()) * constants.MIN_BOUNCE_SPEED
            elif isinstance(platform, Platform):
                normal_dot = self.vel.dot(normal)  # how fast we're moving into the surface
                if abs(normal_dot) < constants.REST_THRESHOLD:
                    # cancel only the into-surface component, no damping
                    self.vel -= normal_dot * normal
                else:
                    #reflect with damping
                    self.vel = self.vel.reflect(normal) * constants.PLATFORM_BOUNCE_MULT

            # step 5: resolve penetration
            distance = pygame.math.Vector2(dx, dy).length()
            penetration = self.radius - distance
            self.pos += normal * (penetration * 1.01)

    
    # checks if there is a collision at a specific position
    # see resolve_collision for proper documentation
    def is_collision(self, player_pos):
        for platform in self.game_state.platforms:
            dist = player_pos - platform.pos
            relative = dist.rotate(-platform.angle)
            closest_x = max(-platform.width/2, min(relative.x, platform.width/2))
            closest_y = max(-platform.height/2, min(relative.y, platform.height/2))
            dx, dy = relative.x - closest_x, relative.y - closest_y
            
            if dx*dx + dy*dy < self.radius*self.radius:
                return platform 
        return False

    # connects to the nearest swing
    def connect(self):
        # if alr connected or no swings, exit
        if self.connection or len(self.game_state.swings) == 0:
            return
        

        # get swing with the lowest distance to the player
        closest_swing = min(
            self.game_state.swings, 
            key=lambda swing: math.dist((self.pos.x, self.pos.y), (swing.pos.x, swing.pos.y))
        )
        
        self.connection = Connector(self.game_state, self, closest_swing)

        # savae length as constant
        self.active_rope_length = (self.pos - closest_swing.pos).length()-15# - min(10, self.vel.length()*0.9)

        # increase velocity along current trajectory
        anchor_pos = self.connection.obj2.pos
        radius_vector = self.pos - anchor_pos
        radius_length = radius_vector.length()

        if radius_length == 0:
            return
        perpendicular_vector = radius_vector.rotate(90)
        self.vel = self.vel.project(perpendicular_vector)
        self.vel *= 1.1
    
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
        new_pos = anchor_pos + (radius_vector.normalize()*self.active_rope_length).rotate(theta)
        
        # step 5: check if this is a valid new position, if not reverse velocity
        col = self.is_collision(new_pos)
        bounce_mult = 1
        match type(col).__name__:
                case "BouncePad":
                    bounce_mult = constants.BOUNCEPAD_BOUNCE_MULT
                case "Platform":
                    bounce_mult = constants.PLATFORM_BOUNCE_MULT

        if col: # there IS a collision
            self.vel *= -1*bounce_mult # adjust velocity for this change
            self.pos = anchor_pos + (radius_vector.normalize()*self.active_rope_length).rotate(-theta) # rotate in opposite dir
        else: # no colliison
            self.pos = new_pos

    def check_death(self):
        if (
            not self.connection
            and self.pos.y > constants.DEATH_BARRIER
            and not self.game_state.game_won
        ):
            audio.play("./assets/audio/scream.mp3", 1, 0)
            time.sleep(1)

            # clear swing (trying to rem bug)
            if self.connection:
                self.game_state.all_sprites.remove(self.connection)
                self.connection = None

            # reset player
            self.pos = pygame.math.Vector2(self.game_state.start_pos)
            self.vel = pygame.math.Vector2(0, 0)
            self.acc = pygame.math.Vector2(0, 0)

            audio.play(audio.music[audio.currentsong].value)
        
    def check_win(self):
        if (
            self.game_state.finish_line 
            and self.pos.x > self.game_state.finish_line.x
        ):
            self.game_state.camera.zoom_to_player()
            
            # slow down for the cinema *fire_emoji**fire_emoji**fire_emoji*
            self.vel *= 0.95
            self.acc = pygame.math.Vector2(0, 0) 
            
            #play win sound
            if self.game_state.game_won == False:
                audio.play("./assets/audio/hey.mp3", 0, 0)
                self.game_state.game_won = True
        
            if self.vel.length() == 0:
                self.game_state.level_loader.load_next_level()
                audio.play(audio.music[audio.currentsong].value)
            
    

    # processes key inputs
    def process_input(self):
        keys = pygame.key.get_pressed()
        
        #if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        #    self.acc.x -= constants.ACCEL
        #if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        #    self.acc.x += constants.ACCEL
        if keys[pygame.K_SPACE] and not self.game_state.game_won:
            self.connect()
        elif self.connection: # if not pressing space, clear connection
            self.game_state.all_sprites.remove(self.connection)
            self.connection = None


    

    

