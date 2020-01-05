import pygame
from os import path
from src.Settings import *
from src.Entity import *


# this function is to load the image file so only load
# once for every scene
def load_image_data(filename):
    # load all the data
    directory = path.dirname(__file__)  # the main directory : src directory
    image_directory = path.join(directory, '../resources/images')  # the image directory : resources/image
    image_data = SpriteSheet(path.join(image_directory, filename))  # the image data name : SpriteSheet()
    return image_data  # image : SpriteSheet()


# this function is to load font
# load once for every scene
def load_font_data(filename, size):
    directory = path.dirname(__file__)  # src directory
    font_directory = path.join(directory, '../resources/fonts')  # resources/fonts
    font_data = pygame.font.Font(path.join(font_directory, filename), size)  # font data
    return font_data  # font data : pygame.font.Font()


# class responsible to load and give all the data in the game
class Data(object):
    def __init__(self):
        self.kenny_future_narrow_font = load_font_data('Kenney Future Narrow.ttf', 20)


# base class for all the scene
class Scene(object):
    def __init__(self, scene_manager):
        self.name = 'null'  # scene name : str
        self.tag = 'null'  # scene tag : str
        self.all_sprites = None  # this is all the sprite in the scene : pygame.sprite.Group()
        self.scene_manager = scene_manager  # get the scene manager to change scene: SceneManger

    # scene base start method
    def start(self):
        pass

    # scene handle events method
    def handle_events(self, event, delta_time):
        pass

    # base scene handle mouse motions
    def handle_mouse_motions(self, event, delta_time, mouse_position):
        pass

    # base scene to handle mouse events
    def handle_mouse_events(self, event, delta_time, mouse_position):
        pass

    # base scene to update
    def update(self, delta_time):
        pass

    # base scene to render
    def render(self, window):
        pass

    # base scene to clear objects
    def clear(self):
        pass


# manage the scene inside the game
class SceneManager(object):
    def __init__(self):
        self.scenes = []  # list of the scenes inside the manager :stack
        self.current_scene_number = 0  # the current scene : int

    # check if the scene manager is empty : boolean
    def is_empty(self):
        return self.scenes == []

    # add the scene to scene manager manually
    def push(self, scene):
        self.scenes.append(scene)  # add the scene inside the collection of scenes
        self.current_scene_number = len(self.scenes) - 1  # change number of current scene to the latest

    # remove scene at the last scene
    def pop(self):
        return self.scenes.pop()

    # check the current scene
    def peek(self):
        return self.scenes[len(self.scenes) - 1]

    # check numbers of scene inside the scenes
    def size(self):
        return len(self.scenes)

    # set the current scene
    # dev's notes :: this function is not make sense
    def set_current_scene(self, scene):
        self.scenes.pop()
        self.scenes.push(scene)  # to push scene??

    def current_scene(self, scene_number):
        self.current_scene_number = scene_number
        return self.scenes[scene_number]

    def get_current_scene_number(self):
        return self.current_scene_number

    def load_scene(self, scene_number):
        self.scenes.pop()  # remove the current scene
        self.scenes.push(scene_number)
        self.scenes[scene_number].start()

    def start(self):
        self.scenes[len(self.scenes) - 1].start()

    def handle_events(self, event, delta_time):
        self.scenes[len(self.scenes) - 1].handle_events(event, delta_time)

    def handle_mouse_motions(self, event, delta_time, mouse_postion):
        self.scenes[len(self.scenes) - 1].handle_mouse_motions(event, delta_time, mouse_postion)

    def handle_mouse_events(self, event, delta_time, mouse_position):
        self.scenes[len(self.scenes) - 1].handle_mouse_events(event, delta_time, mouse_position)

    def update(self, delta_time):
        self.scenes[len(self.scenes) - 1].update(delta_time)

    def render(self, window):
        self.scenes[len(self.scenes) - 1].render(window)

    def clear(self):
        self.scenes[len(self.scenes) - 1].clear()


# class splash screen
# class splash screen will show logo for 5 seconds
class SplashScreen(Scene):
    def __init__(self, scene_manager):
        super().__init__(scene_manager)
        self.name = "Splash Screen"
        self.tag = "Splash Screen"
        self.entities_manager = []

    def start(self):
        pass

    def handle_events(self, event, delta_time):
        pass

    def update(self, delta_time):
        pass

    def render(self, window):
        pass

    def clear(self):
        pass


# class main menu
class MainMenuScene(Scene):
    def __init__(self, scene_manager):
        super().__init__(scene_manager)
        self.name = 'Main Menu '
        self.tag = 'Main Menu'
        self.entities_manager = []
        self.play_button = Entity()
        self.kenny_future_narrow_font = load_font_data('Kenney Future Narrow.ttf', 20)
        self.green_sheet = load_image_data('greenSheet.png')
        self.all_sprites = pygame.sprite.Group()

    def start(self):
        self.play_button.add_component(Button())
        self.play_button.transform.position = WINDOW_CENTER
        self.play_button.get_component(Button()).scene_manager = self.scene_manager
        self.play_button.get_component(Button()).show_rect = False
        self.play_button.add_component(Sprite())
        self.play_button.get_component(Sprite()).set_image(self.green_sheet.get_image(0, 0, 190, 49))
        self.play_button.add_component(Text())
        self.play_button.get_component(Text()).font = self.kenny_future_narrow_font
        self.play_button.get_component(Text()).text = 'PLAY'

        self.entities_manager.append(self.play_button)

        for entity in self.entities_manager:
            entity.start()
            if entity.has_component(Collider()) is True:
                print(entity.gameObject.id)
            if entity.has_component(Sprite()) is True:
                self.all_sprites.add(entity.get_component(Sprite()))

    def handle_events(self, event, delta_time):
        for entity in self.entities_manager:
            entity.handle_events(event, delta_time)

    def handle_mouse_motions(self, event, delta_time, mouse_position):
        for entity in self.entities_manager:
            entity.handle_mouse_motions(event, delta_time, mouse_position)

    def handle_mouse_events(self, event, delta_time, mouse_position):
        for entity in self.entities_manager:
            entity.handle_mouse_events(event, delta_time, mouse_position)

    def update(self, delta_time):
        for entity in self.entities_manager:
            entity.update(delta_time)
        # loop to detect collision
        for i in range(len(self.entities_manager)):
            if self.entities_manager[i].has_component(Collider()):
                # print(self.entities_manager[i].has_component(Collider()))
                for j in range(len(self.entities_manager)):
                    if self.entities_manager[j].has_component(Collider()):
                        if self.entities_manager[i].gameObject.id != self.entities_manager[j].gameObject.id:
                            self.entities_manager[i].get_component(Collider()).collision_detection(
                                self.entities_manager[j].get_component(Collider()).rect)

    # self.all_sprites.update(delta_time)

    def render(self, window):
        window.fill(LIGHTGRAY)
        self.all_sprites.draw(window)
        for entity in self.entities_manager:
            entity.render(window)
        self.draw_center(window)

    def clear(self):
        pygame.display.flip()

    # draw the center on the window
    def draw_center(self, window):
        pygame.draw.line(window, PINK, (0, HEIGHT / 2), (WIDTH, HEIGHT / 2))
        pygame.draw.line(window, PINK, (WIDTH / 2, 0), (WIDTH / 2, HEIGHT))


# class play scene
class PlayScene(Scene):
    def __init__(self, scene_manager):
        super().__init__(scene_manager)
        self.name = 'Play Scene'
        self.tag = 'Play Scene'
        self.entities_manager = []
        self.player = Entity()
        self.wall = Entity()
        self.wall2 = Entity()
        self.sokoban_spritesheet = load_image_data('sokoban_spritesheet@2.png')
        self.all_sprites = pygame.sprite.Group()

    def start(self):

        self.player.transform.position = (400, 400)

        # self.player.add_component(Image())
        # self.player.add_component(Collider())
        # self.player.get_component(Image()).set_image_path('../resources/Player/player_03.png')
        self.player.transform.width = 64
        self.player.transform.height = 64
        self.player.add_component(Sprite())
        self.player.get_component(Sprite()).set_image(self.sokoban_spritesheet.get_image(994, 988, 92, 108))
        self.player.get_component(Sprite()).image.set_colorkey(BLACK)
        self.player.add_component(Movement())
        self.player.add_component(Collider())

        # self.player.add_component(Movement())
        # self.player.add_component(Movement())
        # self.player.get_component(Collider()).show_rect = False

        self.wall.gameObject.tag = 'wall 1'
        self.wall.transform.position = (0, 0)
        self.wall.add_component(Collider())
        self.wall.transform.width = 64
        self.wall.transform.height = 64
        self.wall.add_component(Movement())
        self.wall.add_component(Image())
        self.wall.get_component(Image()).set_image(self.sokoban_spritesheet.get_image(994, 988, 92, 108))
        self.wall.get_component(Image()).image.set_colorkey(BLACK)

        self.wall.get_component(Collider()).show_rect = False
        self.wall.get_component(Movement()).is_mouse = True
        # print(self.wall.get_component(Movement()).is_mouse)

        self.wall2.gameObject.tag = 'wall 2'
        self.wall2.transform.position = (0, 0)
        self.wall2.add_component(Collider())
        self.wall2.transform.width = 64
        self.wall2.transform.height = 64

        # self.player.get_component(Movement()).transform = self.player.transform

        self.entities_manager.append(self.player)
        self.entities_manager.append(self.wall)
        self.entities_manager.append(self.wall2)

        for entity in self.entities_manager:
            entity.start()
            if entity.has_component(Collider()) is True:
                print(entity.gameObject.id)
            if entity.has_component(Sprite()) is True:
                self.all_sprites.add(entity.get_component(Sprite()))

    def handle_events(self, event, delta_time):
        for entity in self.entities_manager:
            entity.handle_events(event, delta_time)

    def handle_mouse_motions(self, event, delta_time, mouse_position):
        for entity in self.entities_manager:
            entity.handle_mouse_motions(event, delta_time, mouse_position)

    def handle_mouse_events(self, event, delta_time, mouse_position):
        for entity in self.entities_manager:
            entity.handle_mouse_events(event, delta_time, mouse_position)

    def update(self, delta_time):
        for entity in self.entities_manager:
            entity.update(delta_time)
        # loop to detect collision
        for i in range(len(self.entities_manager)):
            if self.entities_manager[i].has_component(Collider()):
                # print(self.entities_manager[i].has_component(Collider()))
                for j in range(len(self.entities_manager)):
                    if self.entities_manager[j].has_component(Collider()):
                        if self.entities_manager[i].gameObject.id != self.entities_manager[j].gameObject.id:
                            self.entities_manager[i].get_component(Collider()).collision_detection(
                                self.entities_manager[j].get_component(Collider()).rect)
        self.all_sprites.update(delta_time)

    def render(self, window):
        window.fill(LIGHTBLUE)
        for entity in self.entities_manager:
            entity.render(window)
        self.all_sprites.draw(window)
        self.draw_grid(window)

    def clear(self):
        pygame.display.flip()

    def draw_grid(self, window):
        for x in range(0, WIDTH, TILESIZE):
            pygame.draw.line(window, LIGHTGRAY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pygame.draw.line(window, LIGHTGRAY, (0, y), (WIDTH, y))
