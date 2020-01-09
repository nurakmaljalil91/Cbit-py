import pygame
from os import path
from src.Settings import *
from src.Entity import *
from src.Entity import Entity
from src.Map import *


# this function is to load the image file so only load
# once for every scene
def load_sprite_data(filename):
    # load all the data
    directory = path.dirname(__file__)  # the main directory : src directory
    sprite_directory = path.join(directory, '../resources/spritesheets')  # the image directory : resources/image
    sprite_data = SpriteSheet(path.join(sprite_directory, filename))  # the image data name : SpriteSheet()
    return sprite_data  # image : SpriteSheet()


# this function is to load font
# load once for every scene
def load_font_data(filename, size):
    directory = path.dirname(__file__)  # src directory
    font_directory = path.join(directory, '../resources/fonts')  # resources/fonts
    font_data = pygame.font.Font(path.join(font_directory, filename), size)  # font data
    return font_data  # font data : pygame.font.Font()


# load only single image (not a spritesheet)
def load_single_image_data(filename):
    directory = path.dirname(__file__)  # src directory
    image_directory = path.join(directory, '../resources/images')  # resources /images
    image_data = pygame.image.load(path.join(image_directory, filename))  # load the image
    return image_data  # image data : image


# load map file
def load_map_data(filename):
    directory = path.dirname(__file__)  # src directory
    map_directory = path.join(directory, '../resources/tilemaps')
    map_data = TiledMap(path.join(map_directory, filename))
    return map_data


# function responsible draw center at the window
def draw_center(window):
    pygame.draw.line(window, PINK, (0, HEIGHT / 2), (WIDTH, HEIGHT / 2))
    pygame.draw.line(window, PINK, (WIDTH / 2, 0), (WIDTH / 2, HEIGHT))


def draw_grid(window):
    for x in range(0, WIDTH, TILESIZE):
        pygame.draw.line(window, LIGHTGRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, TILESIZE):
        pygame.draw.line(window, LIGHTGRAY, (0, y), (WIDTH, y))


# class responsible to load and give all the data in the game
class Data(object):
    def __init__(self):
        self.kenny_future_narrow_font = load_font_data('Kenney Future Narrow.ttf', 20)  # load font
        self.play_map = load_map_data('play_scene.tmx')
        self.play_map_image = self.play_map.make_map()
        self.play_map_rect = self.play_map_image.get_rect()


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


# new scene manager
class SceneManager(object):
    def __init__(self):
        self.scenes = {}  # dictionary of the scenes
        self.current_scene = 0
        self.key = 0

    # add scene to the scenes
    def add(self, scene):
        self.scenes[self.key] = scene
        self.key += 1

    # remove scene by key
    def remove(self, key):
        del self.scenes[key]

    # check the length of the scenes
    def length(self):
        return len(self.scenes)

    # load the scene by key
    def load(self, current_scene):
        self.current_scene = current_scene
        self.scenes.get(self.current_scene).start()

    # check if the scene manager is empty : boolean
    def is_empty(self):
        return self.scenes == {}

    # start scene
    def start(self):
        self.scenes.get(self.current_scene).start()

    def handle_events(self, event, delta_time):
        self.scenes[self.current_scene].handle_events(event, delta_time)

    def handle_mouse_motions(self, event, delta_time, mouse_postion):
        self.scenes[self.current_scene].handle_mouse_motions(event, delta_time, mouse_postion)

    def handle_mouse_events(self, event, delta_time, mouse_position):
        self.scenes[self.current_scene].handle_mouse_events(event, delta_time, mouse_position)

    def update(self, delta_time):
        self.scenes[self.current_scene].update(delta_time)

    def render(self, window):
        self.scenes[self.current_scene].render(window)


# class splash screen
# class splash screen will show logo for 5 seconds
class SplashScreen(Scene):
    def __init__(self, scene_manager):
        super().__init__(scene_manager)
        self.name = "Splash Screen"
        self.tag = "Splash Screen"
        self.entities_manager = EntitiesManager()
        self.cbit_logo = Entity()
        self.time_to_fade = 5  # 5 seconds before change scene

    def start(self):
        self.cbit_logo.add_component(Image())
        self.cbit_logo.transform.position = WINDOW_CENTER
        self.cbit_logo.get_component(Image()).image = load_single_image_data('cbit-py-logo.png')

        self.entities_manager.add(self.cbit_logo)

    def handle_events(self, event, delta_time):
        self.entities_manager.handle_events(event, delta_time)

    def update(self, delta_time):
        self.time_to_fade -= delta_time
        if self.time_to_fade <= 0:
            # TODO: change scene
            self.scene_manager.load(1)

        self.entities_manager.update(delta_time)

    def render(self, window):
        window.fill(WHITE)
        self.entities_manager.render(window)
        # draw_center(window)


# class main menu
class MainMenuScene(Scene):
    def __init__(self, scene_manager):
        super().__init__(scene_manager)
        self.name = 'Main Menu '
        self.tag = 'Main Menu'
        self.entities_manager = EntitiesManager()
        self.play_button = Entity()
        self.data = Data()
        self.kenny_future_narrow_font = load_font_data('Kenney Future Narrow.ttf', 20)
        self.green_sheet = load_sprite_data('greenSheet.png')
        self.all_sprites = pygame.sprite.Group()

    def start(self):
        self.play_button.add_component(Button())
        self.play_button.transform.position = WINDOW_CENTER
        self.play_button.get_component(Button()).scene_manager = self.scene_manager
        self.play_button.get_component(Button()).show_rect = False
        self.play_button.add_component(Sprite())
        self.play_button.get_component(Sprite()).set_default_image(self.green_sheet.get_image(0, 0, 190, 49))
        self.play_button.add_component(Text())
        self.play_button.get_component(Text()).font = self.data.kenny_future_narrow_font
        self.play_button.get_component(Text()).text = 'PLAY'

        self.entities_manager.add(self.play_button)

    def handle_events(self, event, delta_time):
        self.entities_manager.handle_events(event, delta_time)

    def handle_mouse_motions(self, event, delta_time, mouse_position):
        self.entities_manager.handle_mouse_motions(event, delta_time, mouse_position)

    def handle_mouse_events(self, event, delta_time, mouse_position):
        self.entities_manager.handle_mouse_events(event, delta_time, mouse_position)

    def update(self, delta_time):
        self.entities_manager.update(delta_time)
        if self.play_button.get_component(Button()).is_pressed:
            self.scene_manager.load(2)  # change scene

    def render(self, window):
        window.fill(LIGHTGRAY)
        self.entities_manager.render(window)
        draw_center(window)


# class play scene
class PlayScene(Scene):
    def __init__(self, scene_manager):
        super().__init__(scene_manager)
        self.name = 'Play Scene'
        self.tag = 'Play Scene'
        self.entities_manager = EntitiesManager()
        self.data = Data()
        self.player = Entity()
        self.wall2 = Entity()
        self.sokoban_spritesheet = load_sprite_data('sokoban_spritesheet@2.png')
        self.all_sprites = pygame.sprite.Group()
        self.camera = Camera(self.data.play_map.width,self.data.play_map.height)

    def start(self):
        self.player.transform.position = (400, 400)
        self.player.transform.width = 100
        self.player.transform.height = 100
        self.player.add_component(Sprite())
        self.player.get_component(Sprite()).set_image(self.sokoban_spritesheet.get_image(994, 988, 92, 108))
        self.player.get_component(Sprite()).image.set_colorkey(BLACK)
        self.player.add_component(Movement())

        self.wall2.gameObject.tag = 'wall 2'
        self.wall2.transform.position = (0, 0)
        self.wall2.add_component(Collider())
        self.wall2.transform.width = 64
        self.wall2.transform.height = 64

        self.entities_manager.add(self.player)
        self.entities_manager.add(self.wall2)

    def handle_events(self, event, delta_time):
        self.entities_manager.handle_events(event, delta_time)

    def handle_mouse_motions(self, event, delta_time, mouse_position):
        self.entities_manager.handle_mouse_motions(event, delta_time, mouse_position)

    def handle_mouse_events(self, event, delta_time, mouse_position):
        self.entities_manager.handle_mouse_events(event, delta_time, mouse_position)

    def update(self, delta_time):
        self.entities_manager.update(delta_time)
        self.camera.update(self.player)

    def render(self, window):
        window.fill(LIGHTBLUE)
        window.blit(self.data.play_map_image, (0, 0))
        self.entities_manager.render(window)
        # draw_grid(window)
