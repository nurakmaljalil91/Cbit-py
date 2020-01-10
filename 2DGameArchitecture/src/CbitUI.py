import pygame
from src.Settings import *

# vector2 : vector2(x,y)
vector2 = pygame.math.Vector2


# base class for all the ui rectangle
class CbitUI(object):
    def __init__(self, x, y, w, h):
        self.position = vector2(x, y)  # position of the ui
        self.width = w  # width of the ui
        self.height = h  # height of the ui
        self.scale = vector2(1, 1)
        self.rotation = vector2(0, 0)
        self.rect = pygame.Rect(self.position[0], self.position[1], self.width, self.height)
        # self.dest_rect = pygame.Rect(self.position[0], self.position[1], self.width, self.height)

        self.thickness = 1

        self.font = pygame.font.SysFont("comicsansms", 32)

        self.show_text = False
        self.can_drag = False
        self.can_resize = False

    def start(self):
        pass

    def handle_events(self, event, delta_time):
        pass

    def update(self, delta_time):
        self.update_center()

    def render(self, window):
        pygame.draw.rect(window, GREEN, self.rect, self.thickness)

    def update_rectangle(self):
        self.rect.center = self.position
        self.rect.w = self.width * self.scale[0]
        self.rect.h = self.height * self.scale[1]

    def update_description(self):
        text_convert = 'rect : (' + str(self.rect.center[0]) + "," + str(self.rect.center[1]) + ')'
        self.text = self.font.render(text_convert, True, BLACK)

    def drag(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.can_drag = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.can_drag = False

        if self.can_drag:
            self.position = pygame.mouse.get_pos()

    def resize(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:
                self.can_resize = True
                print(self.scale)
            else:
                self.can_resize = False
        elif event.type == pygame.KEYUP:
            self.can_resize = False
        if self.can_resize:
            self.scale[0] += 0.1


class Canvas(CbitUI):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)

    def handle_events(self, event, delta_time):
        self.drag(event)
        self.resize(event)

    def update(self, delta_time):
        self.update_rectangle()
        self.update_description()

    def render(self, window):
        pygame.draw.rect(window, GREEN, self.rect, self.thickness)
        pygame.draw.circle(window, GREEN, self.rect.center, 5)
        window.blit(self.text, (self.rect.x + 10, self.rect.y + 10))


class Label(CbitUI):
    def __init__(self, x, y, w, h, canvas):
        super().__init__(x, y, w, h)
        self.canvas = canvas  # canvas where the label attach
        self.label_text = self.font.render('text', True, BLACK)
        self.width, self.height = self.font.size('text')
        self.centerX = self.position[0] - self.width / 2
        self.centerY = self.position[1] - self.height / 2

    def update(self, delta_time):
        self.update_rectangle()
        self.update_description()

    def render(self, window):
        pygame.draw.rect(window, WHITE, self.rect, self.thickness)
        pygame.draw.circle(window, WHITE, self.rect.center, 5)
        window.blit(self.text, (self.rect.x , self.rect.y - 25))
        window.blit(self.label_text, (self.centerX,self.centerY))

    def set_text(self, text=''):
        self.label_text = self.font.render(text, True, BLACK)
        self.width, self.height = self.font.size(text)
        self.centerX = self.position[0] - self.width / 2
        self.centerY = self.position[1] - self.height / 2
