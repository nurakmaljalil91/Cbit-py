from src.entity import EntitiesManager
from src.scene import *
from src.settings import *
from sandbox.player import *


class PlayScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.name = 'Play Scene'
        self.tag = 'Play Scene'
        self.entities_manager = EntitiesManager()
        self.player = Player(self.game)

    def start(self):
        self.entities_manager.add(self.player)

    def handle_events(self, event, delta_time):
        self.entities_manager.handle_events(event, delta_time)

    def update(self, delta_time):
        self.entities_manager.update(delta_time)

    def render(self, window):
        window.fill(LIGHTGRAY)
        self.entities_manager.render(window)
