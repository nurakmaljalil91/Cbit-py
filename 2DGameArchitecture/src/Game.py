import pygame
from src.Entity import *
from src.Scene import *
from sandbox.PlayScene import *
from src.Application import *


class Asset(object):
    def __init__(self):
        self.kenny_future_narrow_font = load_font_data('Kenney Future Narrow.ttf', 20)  # load font
        self.play_map = load_map_data('play_scene.tmx')
        self.play_map_image = self.play_map.make_map()
        self.play_map_rect = self.play_map_image.get_rect()
        self.green_sheet = load_sprite_data('greenSheet.png')
        self.sokoban_spritesheet = load_sprite_data('sokoban_spritesheet@2.png')


# class game
class Game(object):
    def __init__(self, title, width, height, fullscreen):
        # define game attributes
        self.title = title  # title of the game : str
        self.width = width  # screen width : int
        self.height = height  # screen height : int
        self.fullscreen = fullscreen  # check if the window is fullscreen : bool
        self.is_running = None  # check if the game is running : bool
        self.clock = None  # timer or clock getting from pygame :float
        self.delta_time = None  # delta time for the game : float
        self.fps_text = None  # fps text show :font
        self.fps_number = None
        self.asset = None  # all asset for the game is load once inside the game
        # scene properties
        self.scene_manager = None  # declaration of scene manager : SceneManager()
        self.play_scene = None  # declaration of play scene : PlayScene()
        self.main_menu_scene = None  # declaration of main menu scene : MainMenuScene()
        self.splash_screen = None  # declaration of splash screen scene : SplashScreenScene()
        self.test_scene = None  # declaration of test scene : TestScene()
        self.test_scene2 = None  # declaration of test scene : TestScene2()

        # Initialize the pygame(important to use pygame functions)
        pygame.init()  # initialize pygame

        # setting the game window
        # if the fullscreen is true -> window set as fullscreen
        if fullscreen is True:
            self.window = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)
        else:
            self.window = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        pygame.display.set_caption(self.title)  # set the title for the game
        print('[INFO] Game::Game is created')

    # start allow the game to initialize everything
    def start(self):
        # starting the game
        self.is_running = True
        self.asset = Asset()  # initialize the game asset
        self.data = Data()  # initialize the game data
        # starting the clock
        self.clock = pygame.time.Clock()

        # allow the key press hold
        pygame.key.set_repeat(100, 100)

        self.scene_manager = SceneManager()  # create scene manager
        self.play_scene = PlayScene(self)  # create play scene
        self.main_menu_scene = MainMenuScene(self)  # create main menu scene
        self.splash_screen = SplashScreen(self)  # create splash screen scene
        self.test_scene = TestScene(self)  # create test scene
        self.test_scene2 = TestScene2(self)  # create test scene

        # self.scene_manager.add(self.splash_screen)  # insert splash screen first
        # self.scene_manager.add(self.main_menu_scene)  # insert menu scene inside the scene manager
        # self.scene_manager.add(self.play_scene)  # insert play scene inside scene manager
        self.scene_manager.add(self.test_scene)  # insert test scene inside scene manager
        self.scene_manager.add(self.play_scene)  # insert test scene inside scene manager

        # check if the scene manager is not empty
        if self.scene_manager.is_empty() is False:
            self.scene_manager.start()  # start the scene inside scene manager

    # function to handle all the events in the game
    def handle_events(self):
        self.delta_time = self.clock.tick(60) / 1000  # delta time in seconds : float
        self.fps_number = int(self.delta_time * 1000)
        self.fps_text = self.data.kenny_future_narrow_font.render('FPS ' + str(self.fps_number), True, BLACK)

        for event in pygame.event.get():  # check every events in pygame
            if event.type == pygame.QUIT:  # quit the game press x in window
                self.is_running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # quit the game using escape button
                    self.is_running = False
            if self.scene_manager.is_empty() is False:
                self.scene_manager.handle_events(event, self.delta_time)  # handle the scene events

    # function to update all object happen in the game
    def update(self):
        if self.scene_manager.is_empty() is False:
            self.scene_manager.update(self.delta_time)  # update the scenes inside scene manager

    # function to render all object in the game screen
    def render(self):
        if self.scene_manager.is_empty() is False:
            self.scene_manager.render(self.window)  # draw image inside the scene
        self.window.blit(self.fps_text, (10, 10))  # draw fps text

    # function to clear the screen (update the screen)
    # do not make this static
    def clear(self):
        pygame.display.flip()
        pygame.display.update()

    # function to quit the game
    def quit(self):
        pygame.quit()  # quit the game
