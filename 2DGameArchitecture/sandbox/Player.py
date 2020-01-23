from src.Component import *
from src.Entity import *
from src.Settings import *
from src.Game import *
from enum import Enum


class State(Enum):
    FRONT_IDLE = 1
    BACK_IDLE = 2


class Player(Entity):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.gameObject.name = 'Player'
        self.gameObject.tag = 'Player'
        self.transform.position = WINDOW_CENTER
        self.front_idle_animation = []
        self.back_idle_animation = []
        self.current_sprite = 0
        self.last_update = 0

    def start(self):
        self.add_component(Sprite())
        self.get_component(Sprite()).set_sprite(self.game.asset.sokoban_spritesheet.get_image(994, 988, 92, 108))
        self.front_idle_animation.append(self.game.asset.sokoban_spritesheet.get_image(994, 988, 92, 108))
        self.front_idle_animation.append(self.game.asset.sokoban_spritesheet.get_image(994, 880, 92, 108))

    def update(self, delta_time):
        self.animation(delta_time)
        self.get_component(Sprite()).set_sprite(self.front_idle_animation[self.current_sprite])

    def animation(self, delta_time):
        now = pygame.time.get_ticks()
        if now - self.last_update > 180:
            self.last_update = now
            self.current_sprite = (self.current_sprite + 1) % len(self.front_idle_animation)

