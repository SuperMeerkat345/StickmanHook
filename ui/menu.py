import pygame

import utils.constants as constants

class Menu:
    def __init__(self, game_state):
        self.game_state = game_state

        # drawing
        self.surf = pygame.Surface((constants.VIRTUAL_WIDTH, constants.VIRTUAL_HEIGHT), pygame.SRCALPHA)
        self.rect = self.surf.get_rect()
        self.fill = (35, 35, 35, 150)

        self.font = pygame.font.SysFont("Arial", 40)
        self.visible = False

    def handle_event(self, event):
        pass
    
    def draw(self):
        self.surf.fill(self.fill)

        text = self.font.render("TEST_MENU", True, (255,255,255))
        self.surf.blit(text, (300, 100))

        self.game_state.displaysurface.blit(self.surf, self.rect)

    def update(self):
        pass

        
