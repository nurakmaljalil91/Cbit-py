import pygame

from src.Settings import *
from src.Entity import *
from src.Game import *

# vector2 : vector2(x,y)
vector2 = pygame.math.Vector2


# component base class
class Component(object):
    def __init__(self):
        self.id = 0  # component identifier : int
        self.key = 'None'  # component key identifier : str
        self.entity: Entity = None  # entity where this component attach

    def start(self):
        pass

    def handle_events(self, event, delta_time):
        pass

    def update(self, delta_time):
        pass

    def render(self, window):
        pass


class Sprite(Component, pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        self.id = 1
        self.key = 'Sprite'
        self.image = pygame.image.load('../resources/images/box.png')
        self.rect = self.image.get_rect()
        self.show_rect = False
        self.is_animated = False

    def start(self):
        self.rect = self.entity.rect

    def update(self, delta_time):
        self.rect = self.image.get_rect()
        self.rect.x = self.entity.transform.position[0] - self.rect.width / 2
        self.rect.y = self.entity.transform.position[1] - self.rect.height / 2

    def render(self, window):
        if self.show_rect:
            pygame.draw.rect(window, BLUE, self.rect, 2)

    def set_sprite(self, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = self.entity.transform.position[0] - self.rect.width / 2
        self.rect.y = self.entity.transform.position[1] - self.rect.height / 2
        self.image.set_colorkey(BLACK)


class SpriteAnimation(Component):
    def __init__(self):
        super().__init__()
        self.id = 2
        self.key = 'SpriteAnimation'


class Collider(Component):
    def __init__(self):
        super().__init__()
        self.id = 3
        self.key = 'Collider'
        self.rect = None
        self.other_colliders = []
        self.show_rect = True
        self.velocity = vector2(0, 0)

    def start(self):
        self.rect = pygame.Rect(self.entity.transform.position[0], self.entity.transform.position[1],
                                self.entity.transform.width,
                                self.entity.transform.height)

    def handle_events(self, event, delta_time):
        pass

    def update(self, delta_time):
        self.rect = pygame.Rect(self.entity.transform.position[0], self.entity.transform.position[1],
                                self.entity.transform.width,
                                self.entity.transform.height)

    def render(self, window):
        if self.show_rect is True:
            pygame.draw.rect(window, BLUE, self.rect)

    def collision_detection(self, other_collider):
        if self.rect.colliderect(other_collider):
            print(self.gameObject.tag)


class Image(Component):
    def __init__(self):
        super().__init__()
        self.id = 4
        self.key = 'Image'
        self.image = None  # the image of the entity
        self.center = None

    def start(self):
        pass

    def update(self, delta_time):
        if self.image is not None:
            self.center = vector2(self.image.get_rect().w / 2, self.image.get_rect().h / 2)
        # print(self.center.x)
        self.position = vector2(self.entity.transform.position[0] - self.center[0],
                                self.entity.transform.position[1] - self.center[1])
        # self.position[1] = self.entity.transform.position[1] - self.center[1]
        # print(self.entity.transform.position.x)

    def render(self, window, position, width, height):
        window.blit(self.image, self.position)

    def set_image_path(self, path):
        self.image = pygame.image.load(path)

    def set_image(self, image):
        # self.image = pygame.image.load(path)
        self.image = image
        # self.image.set_colorkey(BLACK)

    def change_size(self):
        if self.image is not None:
            if self.transform is not None:
                self.image = pygame.transform.scale(self.image.convert_alpha(),
                                                    (self.transform.width, self.transform.height))


class Movement(Component):
    def __init__(self):
        super().__init__()
        self.id = 5
        self.key = 'Movement'

        self.velocity = vector2(0, 0)
        self.acceleration = vector2(0, 0)
        self.speed = 1000
        self.horizontal = 0
        self.vertical = 0
        self.is_keyboard = True
        self.is_mouse = False

    def start(self):
        pass

    def handle_events(self, event, delta_time):
        if self.is_keyboard is True:
            self.move(event, delta_time, self.transform)

    def handle_mouse_events(self, event, delta_time, mouse_position):
        if self.is_mouse is True:
            self.move_using_mouse(event, delta_time, self.transform, mouse_position)

    def update(self, delta_time):
        # print(self.transform.position)
        pass

    def render(self, window, position: vector2, width, height):
        pass

    def move(self, event, delta_time, transform):
        self.horizontal, self.vertical = 0, 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_s]:
            # self.acceleration.y = 0.5
            # self.velocity = vector2(0, 0.1)
            self.vertical = 1
        if keystate[pygame.K_w]:
            # self.acceleration.y = -0.5
            # self.velocity = vector2(0, -0.1)
            self.vertical = -1
        if keystate[pygame.K_a]:
            # self.acceleration.x = -0.5
            # self.velocity = vector2(-0.1, 0)
            self.horizontal = -1
        if keystate[pygame.K_d]:
            # self.acceleration.x = 0.5
            # self.velocity = vector2(0.1, 0)
            self.horizontal = 1
        if self.horizontal != 0 and self.vertical != 0:
            self.horizontal /= 1.414
            self.vertical /= 1.414
        # self.velocity += self.acceleration
        # self.transform.position += self.velocity
        # self.transform.position += self.velocity * self.speed * delta_time
        self.entity.transform.position += vector2(self.horizontal, self.vertical) * self.speed * delta_time

    def move_using_mouse(self, event, delta_time, transform, mouse_position):

        if event.button == 1:
            print(event)

            if self.transform.position != mouse_position:
                self.transform.position = mouse_position
