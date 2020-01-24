import pygame


class Input(object):
    def __init__(self):
        self.keys = pygame.key.get_focused()
        self.event = None

    def set(self, event: pygame.event):
        self.event = event

    def get_axis(self, direction: str):
        int_direction = 0
        if self.event is pygame.KEYDOWN:
            if direction is 'vertical':
                if self.event is pygame.K_LEFT:
                    int_direction = 1
                if self.event is pygame.K_RIGHT:
                    int_direction = -1
            if direction is 'horizontal':
                if self.event is pygame.K_DOWN:
                    int_direction = 1
                if self.event is pygame.K_UP:
                    int_direction = -1
        return int_direction
