import pygame
import random
import string
from src.component import *
from src.settings import *


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


# class sprite sheet
class SpriteSheet(object):
    # utility class for loading and passing images
    def __init__(self, filename):
        # take the image as the sprite sheet : pygame.image.load()
        # If you want to change a 24-bit image to 32-bit or vice versa, use the .convert_alpha() method.
        # For vice-versa, use the .convert() method which will overlay any per-pixel alpha values over black.
        self.spritesheet = pygame.image.load(filename).convert_alpha()

    # get the single image from the sprite sheet
    def get_image(self, x, y, width, height):
        # grab an image out of a larger spritesheet
        image = pygame.Surface((width, height))  # get the image surface
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))  # bilt only part of the image
        # image = pygame.transform.scale(image, (width // 2, height // 2))  # scale the image to half size
        return image  # return image


# class transform responsible to determine entity position and size
# very important component
class Transform(object):
    def __init__(self):
        self.position = vector2(0, 0)  # position of the entity : vector2(x,y)
        self.scale = vector2(0, 0)
        self.rotation = vector2(0, 0)


# class or component gameobject to determine the entity name and existence
class GameObject(object):
    def __init__(self):
        self.name = ''  # name : str
        self.tag = ''  # tag : str
        self.id = generate_id()  # generate random id
        self.active = True  # check if active self : boolean


# class entity
class Entity(object):
    def __init__(self):
        self.gameObject = GameObject()  # add component game object
        self.transform = Transform()  # add component transform
        self.components = {}  # list of the components in the entity : dictionary{key:value}
        self.rect = pygame.Rect(self.transform.position[0], self.transform.position[1], TILESIZE, TILESIZE)

    # add component to the entity
    def add_component(self, component: Component):
        key = component.key  # get key from component key : str
        # only allow one same component to the entity
        if key in self.components.keys():
            print('[INFO] Entity::78:: Component already exist inside the Entity!, cannot add Component')
        else:
            component.entity = self  # make the component entity this entity
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

    # function of start the components for the entity
    def start(self):
        for component in self.components.values():
            component.start()

    # function to handle events in the components for the entity
    def handle_events(self, event, delta_time):
        if self.gameObject.active:
            for component in self.components.values():
                component.handle_events(event, delta_time)

    # function to update all the process of the entity
    def update(self, delta_time):
        if self.gameObject.active:
            # update all the components attach to the entity
            for component in self.components.values():
                component.update(delta_time)

    # function to render image for the entity
    def render(self, window):
        if self.gameObject.active:
            for component in self.components.values():
                component.render(window)


# class responsible to manage all entities
class EntitiesManager(object):
    def __init__(self):
        self.entities = []  # list of entities
        self.sprites_group = pygame.sprite.Group()  # get the sprite group

    # add entity into the entities
    def add(self, entity: Entity):
        self.entities.append(entity)  # add entity inside the entities
        entity.start()  # start the entity
        if entity.has_component(Collider()) is True:
            print(entity.gameObject.id)
        if entity.has_component(Sprite()) is True:
            self.sprites_group.add(entity.get_component(Sprite()))

    # function to handle events for all the entities
    def handle_events(self, event, delta_time):
        for entity in self.entities:
            entity.handle_events(event, delta_time)

    # function to update all the entities
    def update(self, delta_time):
        for entity in self.entities:
            entity.update(delta_time)
        # loop to detect collision
        for i in range(len(self.entities)):
            if self.entities[i].has_component(Collider()):
                # print(self.entities_manager[i].has_component(Collider()))
                for j in range(len(self.entities)):
                    if self.entities[j].has_component(Collider()):
                        if self.entities[i].gameObject.id != self.entities[j].gameObject.id:
                            self.entities[i].get_component(Collider()).collision_detection(
                                self.entities[j].get_component(Collider()).rect)
        # update sprite group
        self.sprites_group.update(delta_time)

    # function to render all the entities
    def render(self, window):
        self.sprites_group.draw(window)
        for entity in self.entities:
            entity.render(window)

    # function to clear and remove all the entities
    def clean(self):
        self.entities.clear()
        del self.entities[:]
