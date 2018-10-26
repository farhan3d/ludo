import pygame


SCREEN_SIZE = [600, 600]
ROW_COUNT = 15
TILE_BOUNDARY_COLOR = (0, 204, 204)
TILE_CENTER_COLOR = (255, 178, 102)
TILE_SIZE = 32
tiles_dict = {} # {tile_num: [location, type, state]}
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
    def __init__(self, screen, size, location_arr, color, state, tile_type):
        self.location = location_arr
        self.color = color
        self.state = state
        self.type = tile_type
        pygame.draw.rect(screen, color, pygame.Rect(location_arr[0],
                                             location_arr[1], size, size), 2)


class Ludo:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_SIZE[0],
                                               SCREEN_SIZE[1]))
        base_size = min(SCREEN_SIZE)
        base_size -= 35
        row_inc = (base_size / ROW_COUNT ) * 0.5
        tile_num = 0
        for row in range(0, ROW_COUNT):
            if (row > 5 and row < 9):
                column_inc = (base_size / ROW_COUNT) * 0.5
                for column in range(0, ROW_COUNT):
                    if (column < 6 or column > 8):
                        if (row == 7):
                            color = TILE_CENTER_COLOR
                            tile_type = 1
                        else:
                            color = TILE_BOUNDARY_COLOR
                            tile_type = 0
                        new_tile = Tile(self.screen, TILE_SIZE, [column_inc,
                                        row_inc], color, 0, tile_type)
                        tiles_dict[tile_num] = new_tile
                        tile_num += 1
                    column_inc += base_size / ROW_COUNT
            else:
                vertical_column_inc = (base_size / ROW_COUNT) * 0.5
                for column in range(0, ROW_COUNT):
                    if (column > 5 and column < 9):
                        if column == 7:
                            color = TILE_CENTER_COLOR
                            tile_type = 1
                        else:
                            color = TILE_BOUNDARY_COLOR
                            tile_type = 0
                        new_tile = Tile(self.screen, TILE_SIZE,
                                        [vertical_column_inc, row_inc], color,
                                        0, tile_type)
                        tiles_dict[tile_num] = new_tile
                        tile_num += 1
                    vertical_column_inc += base_size / ROW_COUNT
            row_inc += base_size / ROW_COUNT


if __name__ == "__main__":
    app = Ludo()
    for tile in tiles_dict:
        print(tiles_dict[tile].location)
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        pygame.display.flip()
        clock.tick(30)
