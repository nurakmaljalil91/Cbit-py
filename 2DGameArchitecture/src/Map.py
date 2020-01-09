import pygame
import pytmx
from src.Settings import *


class TiledMap(object):
    def __init__(self, filename):
        tile_map = pytmx.load_pygame(filename, pixelalpha=True)
        self.width = tile_map.width * tile_map.tilewidth
        self.height = tile_map.height * tile_map.tileheight
        self.tile_map_data = tile_map

    def render(self, window):
        tile_id = self.tile_map_data.get_tile_image_by_gid
        for layer in self.tile_map_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    tile = tile_id(gid)
                    if tile:
                        window.blit(tile, (x * self.tile_map_data.tilewidth, y * self.tile_map_data.tileheight))

    def make_map(self):
        temp_surface = pygame.Surface((self.width, self.height))
        self.render(temp_surface)
        return temp_surface


# class Camera
class Camera(object):
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def set_follow(self, entity):
        return entity.rect.move(self.camera.topleft)

    def set_follow_rect(self, rect):
        return rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.centerx + int(WIDTH / 2)
        y = -target.rect.centery + int(HEIGHT / 2)

        # limit scrolling to map size
        x = min(0, x)  # left
        y = min(0, y)  # top
        x = max(-(self.width - WIDTH), x)  # right
        y = max(-(self.height - HEIGHT), y)  # bottom
        self.camera = pygame.Rect(x, y, self.width, self.height)
