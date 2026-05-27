import pygame

class Menu:
    def __init__(self, game_state):
        self.game_state = game_state

        # drawing
        self.surf = pygame.Surface((constants.VIRTUAL_WIDTH, constants.VIRTUAL_HEIGHT), pygame.SRCALPHA)
        self.rect = self.surf.get_rect(center=(0, 0)) # top_left???
        self.fill = (35, 35, 35, 150)

        self.font = pygame.font.SysFont("Arial", 40)
        self.visible = False

    def handle_event(self, event):
        pass

    def update(self):
        self.surf.fill(self.fill)

        text = self.font.render("TEST_MENU", True, (255,255,255))
        self.surface.blit(text, (300, 100))
