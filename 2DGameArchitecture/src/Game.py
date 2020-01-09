import pygame
from src.Entity import *
from src.Scene import *


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

        # scene properties
        self.scene_manager = None  # declaration of scene manager : SceneManager()
        self.play_scene = None  # declaration of play scene : PlayScene()
        self.main_menu_scene = None  # declaration of main menu scene : MainMenuScene()
        self.splash_screen = None  # declaration of splash screen scene : SplashScreenScene()

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
        self.data = Data()  # initialize the game data
        # starting the clock
        self.clock = pygame.time.Clock()

        # allow the key press hold
        pygame.key.set_repeat(100, 100)

        self.scene_manager = SceneManager()  # create scene manager
        self.play_scene = PlayScene(self.scene_manager)  # create play scene
        self.main_menu_scene = MainMenuScene(self.scene_manager)  # create main menu scene
        self.splash_screen = SplashScreen(self.scene_manager)  # create splash screen scene

        self.scene_manager.add(self.splash_screen)  # insert splash screen first
        self.scene_manager.add(self.main_menu_scene)  # insert menu scene inside the scene manager
        self.scene_manager.add(self.play_scene)  # insert play scene inside scene manager

        # check if the scene manager is not empty
        if self.scene_manager.is_empty() is False:
            self.scene_manager.start()  # start the scene inside scene manager

    # function to handle all the events in the game
    def handle_events(self):
        self.delta_time = self.clock.tick(60) / 1000  # delta time in seconds : float
        self.fps_number = int(self.delta_time * 1000)
        self.fps_text = self.data.kenny_future_narrow_font.render('FPS ' + str(self.fps_number), True, BLACK)
        for event in pygame.event.get():  # check every events in pygame
            mouse_position = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:  # quit the game press x in window
                self.is_running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # quit the game using escape button
                    self.is_running = False
                if self.scene_manager.is_empty() is False:
                    self.scene_manager.handle_events(event, self.delta_time)  # handle the scene events
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.scene_manager.is_empty() is False:
                    self.scene_manager.handle_mouse_events(event, self.delta_time, mouse_position)  # handle the mouse
                    # events
            if event.type == pygame.MOUSEMOTION:
                if self.scene_manager.is_empty() is False:
                    self.scene_manager.handle_mouse_motions(event, self.delta_time, mouse_position)  # handle the
                    # scene mouse motions

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
