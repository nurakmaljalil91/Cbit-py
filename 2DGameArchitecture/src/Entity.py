import pygame
import random
import string
from src.Component import *
from src.Settings import *


# class sprite sheet
class SpriteSheet(object):
    # utility class for loading and passing images
    def __init__(self, filename):
        # take the image as the sprite sheet : pygame.image.load()
        # If you want to change a 24-bit image to 32-bit or vice versa, use the .convert_alpha() method.
        # For vice-versa, use the .convert() method which will overlay any per-pixel alpha values over black.
        self.spritesheet = pygame.image.load(filename).convert()

    # get the single image from the sprite sheet
    def get_image(self, x, y, width, height):
        # grab an image out of a larger spritesheet
        image = pygame.Surface((width, height))  # get the image surface
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))  # bilt only part of the image
        image = pygame.transform.scale(image, (width // 2, height // 2))  # scale the image to half size
        return image  # return image


# this function will generate random id consist of str and int
# need this for collider component
def generate_id():
    random_number = random.randint(100, 999)  # 3 digit random numbers : int
    random_string = ''.join(
        [random.choice(string.ascii_letters) for n in range(3)])  # 3 random alphabets : str
    random_id = random_string + str(random_number)  # append random str and int
    return random_id  # random id : str


# vector2 : vector2(x,y)
vector2 = pygame.math.Vector2


# class transform responsible to determine entity position and size
# very important component
class Transform(object):
    def __init__(self, position: vector2, width, height):
        self.position = position  # position of the entity : vector2(x,y)
        self.width = width  # width of the entity : int
        self.height = height  # height of the entity : int
        self.scale = 1
        self.size = vector2(self.width * self.scale, self.height * self.scale)
        self.center = vector2(self.size.x / 2 + self.position.x, self.size.y / 2 + self.position.y)
        self.marker_image = pygame.image.load('../resources/images/marker2.png')
        self.marker_image_position = vector2((self.position.x + self.width) / 2, self.position.y)

    def update(self):
        self.marker_image_position = vector2((self.position[0] + self.width) / 2, self.position[1])


# class or component gameobject to determine the entity name and existence
class GameObject(object):
    def __init__(self, name, tag):
        self.name = name  # name : str
        self.tag = tag  # name : tag
        self.id = generate_id()  # generate random id
        self.active_self = True  # check if active self : boolean


# class entity
class Entity(object):
    def __init__(self):
        self.gameObject = GameObject('null', 'null')  # add component game object
        self.transform = Transform(vector2(0.0, 0.0), 64, 64)  # add component transform
        self.components = {}  # list of the components in the entity : dictionary{key:value}

    # add component to the entity
    def add_component(self, component: Component):
        key = component.key  # get key from component key : str
        # only allow one same component to the entity
        if key in self.components.keys():
            print('[INFO] Entity::78:: Component already exist inside the Entity!, cannot add Component')
        else:
            component.entity = self
            self.components[key] = component  # add the component in the list of components
            # self.process_all_components(key)  # process all the components that been added to the entity

    # get the component from the entity
    def get_component(self, component: Component):
        key = component.key  # get key from component key : str
        # check if the key is inside the components
        if key not in self.components:
            print('[ERROR] Entity::Component is not inside the components')  # if not inside the components
        else:
            return self.components[key]  # else give back the component

    # check if the entity contain component : bool
    def has_component(self, component: Component):
        key = component.key  # get key from component key : str
        # return self.get_component(component) is not None
        if key in self.components:
            return True
        else:
            return False

    # this is hidden function to make all the component connecting
    # with each other, making this as very important function
    def process_all_components(self, key):
        for key in self.components:
            self.components.get(key).transform = self.transform  # update components transform
            self.components.get(key).gameObject = self.gameObject  # update components game object
        '''
        if key == 'Collider':
            self.components.get(key).transform = self.transform
            self.components.get(key).gameObject = self.gameObject
        if key == 'Sprite':
            self.components.get(key).transform = self.transform
        if key == 'Image':
            self.components.get(key).transform = self.transform
        if key == 'Movement':
            self.components.get(key).transform = self.transform
        if key == 'Button':
            self.components.get(key).transform = self.transform
       
        for key in self.components:
            if key == 'Collider':
                self.components.get(key).transform = self.transform
                self.components.get(key).gameObject = self.gameObject
            if key == 'Image':
                self.components.get(key).transform = self.transform
            if key == 'Movement':
                self.components.get(key).transform = self.transform
        '''

    # function of start the components for the entity
    def start(self):
        for component in self.components.values():
            component.start()

    # function to handle events in the components for the entity
    def handle_events(self, event, delta_time):
        for component in self.components.values():
            component.handle_events(event, delta_time)

    def handle_mouse_motions(self, event, delta_time, mouse_position):
        for component in self.components.values():
            component.handle_mouse_motions(event, delta_time, mouse_position)

    def handle_mouse_events(self, event, delta_time, mouse_position):
        for component in self.components.values():
            component.handle_mouse_events(event, delta_time, mouse_position)

    # function to update all the process of the entity
    def update(self, delta_time):
        # update all the components attach to the entity
        self.transform.update()
        for component in self.components.values():
            component.update(delta_time)

    # function to render image for the entity
    def render(self, window):

        for component in self.components.values():
            component.render(window, self.transform.position, self.transform.width, self.transform.height)
        # print(self.transform.marker_image_position)
        # window.blit(self.transform.marker_image, self.transform.marker_image_position)


class EntitiesManager(object):
    def __init__(self):
        self.entities = []

    def add(self, entity: Entity):
        self.entities.append(entity)
        entity.start()

    def handle_events(self, event, delta_time):
        for entity in self.entities:
            entity.handle_events(event, delta_time)

    def handle_mouse_motions(self, event, delta_time, mouse_position):
        for entity in self.entities:
            entity.handle_mouse_motions(event, delta_time, mouse_position)

    def handle_mouse_events(self, event, delta_time, mouse_position):
        for entity in self.entities:
            entity.handle_mouse_events(event, delta_time, mouse_position)

    def update(self, delta_time):
        for entity in self.entities:
            entity.update(delta_time)

    def render(self, window):
        for entity in self.entities:
            entity.render(window)

    '''
    def clear(self):
        for entity in self.entities:
            entity.clear()
    '''

    def clean(self):
        self.entities.clear()
        del self.entities[:]
