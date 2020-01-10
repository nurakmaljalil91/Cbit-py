import pygame
from src.Settings import *

# vector2 : vector2(x,y)
vector2 = pygame.math.Vector2


# base class for all the ui rectangle
class CbitUI(object):
    def __init__(self, x, y, w, h):
        # main ui rectangle properties
        self.position = vector2(x, y)  # position of the ui
        self._width = w  # width of the ui
        self._height = h  # height of the ui
        self.scale = vector2(1, 1)  # scale of the ui
        self.rotation = vector2(0, 0)  # rotation of the ui

        # create the initial ui rectangle
        self._rect = pygame.Rect(self.position[0], self.position[1], self._width, self._height)
        self.thickness = 1  # thickness of the rect

        # create relative rectangle
        self._rel_rect = pygame.Rect(self.position[0], self.position[1], self._width, self._height)

        self._font = pygame.font.SysFont("Consolas", 32)  # default ui font
        self.text = self._font.render('', True, BLACK)  # render the text
        self._show_text = False  # show the text description of the position
        self._can_drag = False  # rect can be drag
        self._can_resize = False  # rectangle can resize
        self._can_rotate = False  # rectangle can rotate

    # base start function for ui
    def start(self):
        pass

    # base handle events function for ui
    def handle_events(self, event, delta_time):
        pass

    # base update function for ui
    def update(self, delta_time):
        pass

    def render(self, window):
        pass

    # this function is to make sure the rectangle is following the position
    # change position will change the rect position
    # also update the rectangle size
    def update_rectangle(self):
        self._rect.center = self.position  # position of the ui is at the center of the rectangle
        self._rect.w = self._width * self.scale[0]  # update the rectangle width
        self._rect.h = self._height * self.scale[1]  # update the rectangle height

    def get_rect_pos(self):
        return vector2(self._rect.x, self._rect.y)

    # function to get the rect x as rect is protected
    def get_rect_x(self):
        return self._rect[0]

    # function to get the rect y
    def get_rect_y(self):
        return self._rect[1]

    def get_rect_center(self):
        center_x = self._rect[0] - self._width
        center_y = self._rect[1] - self._height
        return center_x, center_y

    # update the relative rectangle
    # def update_relative_rectangle(self, parent):
    #     initial_offset = self.position - parent.get_rect_pos()
    #     final_offset = self.position - parent.get_rect_pos()
    #     if final_offset[0] < initial_offset[0]:
    #         relative_position_x = self.position[0] + (final_offset[0] - initial_offset[0])
    #     if final_offset[0] > initial_offset[0]:
    #         relative_position_x = self.position[0] + (final_offset[0] - initial_offset[0])
    #     if final_offset[1] < initial_offset[1]:
    #         relative_position_y = self.position[1] + (final_offset[1] - initial_offset[1])
    #     if final_offset[0] > initial_offset[0]:
    #         relative_position_y = self.position[1] + (final_offset[1] - initial_offset[1])
    #     else:
    #         relative_position_x = self.position[0] + 0
    #         relative_position_y = self.position[1] + 0
    #
    #     self._rel_rect = pygame.Rect(relative_position_x, relative_position_y, self._rect.w, self._rect.h)

    # function to show position of the rectangle
    def update_show_position(self):
        text_convert = 'rect : (' + str(self._rect.x) + "," + str(
            self._rect.y) + ')'  # update the rect
        self.text = self._font.render(text_convert, True, BLACK)  # render the text

    # set the font to use for the ui
    def set_font(self, font):
        self._font = font

    # this function allow changing the position of the rectangle
    # based on the mouse position
    def drag(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self._rect.collidepoint(event.pos):
                self._can_drag = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self._can_drag = False
        # update the position
        if self._can_drag:
            self.position = pygame.mouse.get_pos()  # position equal mouse position

    # allow the ui to resize
    def resize(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:
                self._can_resize = True
                print(self.scale)
            else:
                self._can_resize = False
        elif event.type == pygame.KEYUP:
            self._can_resize = False
        if self._can_resize:
            self.scale[0] += 0.1


# class responsible to manage all entities
class CbitUIHolder(object):
    def __init__(self):
        self.uis = []  # list of entities
        self.sprites_group = pygame.sprite.Group()  # get the sprite group

    # add entity into the entities
    def add(self, ui: CbitUI):
        self.uis.append(ui)  # add entity inside the entities
        ui.start()  # start the entity

    # function to handle events for all the entities
    def handle_events(self, event, delta_time):
        for ui in self.uis:
            ui.handle_events(event, delta_time)

    # function to update all the entities
    def update(self, delta_time):
        for ui in self.uis:
            ui.update(delta_time)
        # update sprite group
        # self.sprites_group.update(delta_time)

    # function to render all the entities
    def render(self, window):
        # self.sprites_group.draw(window)
        for ui in self.uis:
            ui.render(window)


# Canvas class to hold all the ui inside the window
class Canvas(CbitUI):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)

    # handle all the canvas event
    def handle_events(self, event, delta_time):
        # self.drag(event)
        self.resize(event)

    # update the canvas
    def update(self, delta_time):
        self.update_rectangle()
        self.update_show_position()

    # render the canvas
    def render(self, window):
        pygame.draw.rect(window, GREEN, self._rect, self.thickness)  # draw rect
        pygame.draw.circle(window, GREEN, self._rect.center, 5)  # draw center
        # window.blit(self.text, (self._rect.x + 10, self._rect.y + 10))  # draw show position


# class label
class Label(CbitUI):
    def __init__(self, x, y, w, h, parent):
        super().__init__(x, y, w, h)
        self.parent = parent  # canvas where the label attach
        self._label_text = self._font.render('text', True, BLACK)  # protect label text
        self.text_width, self.text_height = self._font.size('text')  # get the text width and height

    # handle event for label
    def handle_events(self, event, delta_time):
        self.drag(event)

    # update the label
    def update(self, delta_time):
        self.update_rectangle()  # update rectangle of the label
        # self.update_relative_rectangle(self.parent)  # update relative rectangle
        self.update_show_position()  # update show position

    # render the label
    def render(self, window):
        pygame.draw.rect(window, WHITE, self._rect, self.thickness)
        pygame.draw.circle(window, WHITE, self._rect.center, 5)
        window.blit(self.text, (self._rect.x, self._rect.y + 25))

    # set the text for the label
    def set_text(self, text=''):
        self._label_text = self._font.render(text, True, BLACK)
        self.text_width, self.text_height = self._font.size(text)


# class text
class Text(CbitUI):
    def __init__(self, x, y, parent, text):
        super().__init__(x, y, TILESIZE, TILESIZE)
        self.parent = parent  # set the parent of the text
        self._text = text
        self._render_text = self._font.render(self._text, True, BLACK)
        self.color = BLACK  # initialize the font color to black
        self._width, self._height = self._font.size(self._text)

    def update(self, delta_time):
        self.update_rectangle()
        self.update_text()
        # self.update_relative_rectangle(self.parent)

    def render(self, window):
        pygame.draw.rect(window, WHITE, self._rect, self.thickness)
        pygame.draw.circle(window, WHITE, self._rect.center, 5)
        window.blit(self._render_text, (self._rect.x, self._rect.y))

    # set the text for the label
    def set_text(self, text=''):
        self._render_text = self._font.render(text, True, BLACK)
        self._width, self._height = self._font.size(text)

    def update_text(self):
        self._render_text = self._font.render(self._text, True, BLACK)
        self._width, self._height = self._font.size(self._text)


class Image(CbitUI):
    def __init__(self, x, y, parent, image):
        super().__init__(x, y, TILESIZE, TILESIZE)
        self.parent = parent
        self._image = image  # image of the image
        self._rect = self._image.get_rect()

    def update(self, delta_time):
        self._rect[0] = self.position[0]
        self._rect[1] = self.position[1]

    def render(self, window):
        pygame.draw.rect(window, WHITE, self._rect, self.thickness)
        pygame.draw.circle(window, WHITE, self._rect.center, 5)
        window.blit(self._image, (self._rect[0], self._rect[1]))


class Button(CbitUI):
    def __init__(self, x, y, w, h, parent):
        super().__init__(x, y, w, h)
        self.parent = parent
        self.__state = 0  # 0 for normal, 1 for hover, 2 for click

    def handle_events(self, event, delta_time):
        if self._rect.collidepoint(pygame.mouse.get_pos()):
            self.__state = 1
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.__state = 2
                print('click')
            elif event.type == pygame.MOUSEBUTTONUP:
                self.__state = 0
        else:
            self.__state = 0

    def update(self, delta_time):
        pass

    def render(self, window):
        pygame.draw.rect(window, RED, self._rect, self.thickness)
        pygame.draw.circle(window, RED, self._rect.center, 5)
