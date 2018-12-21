import const
import math
import pygame

class Tile:

    def redraw_tile(self, screen):
        pygame.draw.rect(screen, self.color,
                         pygame.Rect(self.location_for_draw[0],
                                     self.location_for_draw[1], const.TILE_SIZE,
                                     const.TILE_SIZE), 2)

    def __init__(self, screen, size, location_arr, color, state, tile_type,
                 is_path=None):
        self.location_for_draw = location_arr
        self.location = [math.ceil(location_arr[0] + const.TILE_SIZE / 2),
                         math.ceil(location_arr[1] + const.TILE_SIZE / 2)]
        self.color = color
        self.state = state
        self.type = tile_type
        self.previous = None
        self.next = None
        self.is_path = is_path
        pygame.draw.rect(screen, color, pygame.Rect(location_arr[0],
                         location_arr[1], size, size), 2)


