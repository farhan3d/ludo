import pygame


SCREEN_SIZE = [600, 600]
ROW_COUNT = 15
TILE_COLOR = (255, 100, 0)
tiles_dict = {} # {tile_num: [location, state]}
done = False


pygame.init()

clock = pygame.time.Clock()


class Player:
    pass


class Piece:
    pass


class Board:
    pass


class Tile:
    def __init__(self, screen=None, size=None, location_arr=None, state=None):
        pygame.draw.rect(screen, TILE_COLOR, pygame.Rect(location_arr[0],
                                             location_arr[1], size, size))


class Ludo:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_SIZE[0],
                                               SCREEN_SIZE[1]))
        base_size = min(SCREEN_SIZE)
        row_inc = (base_size / ROW_COUNT ) * 0.5
        tile_num = 0
        #vertical_column_inc = (base_size / ROW_COUNT) * 0.5
        for row in range(0, ROW_COUNT):
            if (row > 5 and row < 9):
                column_inc = (base_size / ROW_COUNT) * 0.5
                for column in range(0, ROW_COUNT):
                    if (column < 6 or column > 8):
                        new_tile = Tile(self.screen, 10, [column_inc, row_inc])
                        tiles_dict[tile_num] = new_tile
                    column_inc += base_size / ROW_COUNT
            else:
                vertical_column_inc = (base_size / ROW_COUNT) * 0.5
                for column in range(0, ROW_COUNT):
                    if (column > 5 and column < 9):
                        new_tile = Tile(self.screen, 10, [vertical_column_inc, row_inc])
                        tiles_dict[tile_num] = new_tile
                    vertical_column_inc += base_size / ROW_COUNT
            row_inc += base_size / ROW_COUNT


if __name__ == "__main__":
    app = Ludo()
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        pygame.display.flip()
        clock.tick(30)
