import pygame

class Camera:
    def __init__(self, width, height):
        self.offset = pygame.math.Vector2()
        self.width = width
        self.height = height

        self.offset.x = 0
        self.offset.y = 0

    # update camera position to follow a target
    def update(self, target):
        self.offset.x = target.pos.x - self.width//2
        self.offset.y = target.pos.y - self.height//2
    
    # applies camera's offset to the rect of a sprite
    def apply(self, rect):
        # dont apply vertical offset for now...
        return rect.move(-self.offset.x, 0) #rect.move(-self.offset.x, -self.offset.y)

    # applies offset to a position vector
    def apply_pos(self, pos):
        return (
            pos.x - self.offset.x,
            pos.y
        )
    