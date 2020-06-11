import pygame


class Input(object):
    def __init__(self):
        self.keys = pygame.key.get_focused()
        self.event = None
        self.direction = 0

    def set(self, event: pygame.event):
        self.event = event

    def get_axis(self, direction: str):
        if self.event == pygame.KEYDOWN:
            if direction == 'vertical':
                if self.event == pygame.K_LEFT:
                    self.direction = 1
                if self.event == pygame.K_RIGHT:
                    self.direction = -1
            if direction == 'horizontal':
                if self.event == pygame.K_DOWN:
                    self.direction = 1
                if self.event == pygame.K_UP:
                    self.direction = -1
        return self.direction
