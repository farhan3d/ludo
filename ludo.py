import math
import pygame


SCREEN_SIZE = [600, 600]                    # the base canvas size
ROW_COUNT = 15                              # board size adjusts to this value
TILE_BOUNDARY_COLOR = (0, 204, 204)         # color of main movement tiles
TILE_CENTER_COLOR = (255, 178, 102)         # color of the safe zone center tiles
TILE_START_COLOR = (255, 255, 0)            # color of the start tile in tiles linked list
TILE_PATH_MARKER = (255, 0, 255)            # marker color for path tiles
TILE_SIZE = math.floor(ROW_COUNT * 2.25)    # a tile size adjusted from board size
done = False                                # simple little bool to manage game loop


pygame.init()
clock = pygame.time.Clock()


class Player:
    pass


class Piece:
    pass


class Tile:
    def __init__(self, screen, size, location_arr, color, state, tile_type,
                 is_path=None):
        self.location = location_arr
        self.color = color
        self.state = state
        self.type = tile_type
        self.previous = None
        self.next = None
        self.is_path = is_path
        pygame.draw.rect(screen, color, pygame.Rect(location_arr[0],
                         location_arr[1], size, size), 2)
        if self.is_path:
            pygame.draw.rect(screen, color, pygame.Rect(location_arr[0],
                         location_arr[1], size * 0.2, size * 0.2), 2)


class Board:

    """iterate over tiles and link them with each other in order of
    traversal"""
    def post_processing(self):
        previous_tile = None
        for i in range(len(self.tiles_collection)):
            if (self.is_next_by_distance(self.tiles_collection[i],
                self.start_tile) and (self.tiles_collection[i].type == 0)):
                self.start_tile.next == self.tiles_collection[i]
                self.tiles_collection[i].previous == self.start_tile
                previous_tile = self.tiles_collection[i]
                pygame.draw.rect(self.screen, TILE_PATH_MARKER,
                                 pygame.Rect(self.tiles_collection[i].location[0],
                                 self.tiles_collection[i].location[1],
                                 9, 9), 2)
        if previous_tile != None:
            for k in range(len(self.tiles_collection)):
                for j in range(len(self.tiles_collection)):
                    if (self.is_next_by_distance(self.tiles_collection[j],
                        previous_tile) and (self.tiles_collection[j].is_path == True) and
                        (self.tiles_collection[j].next == None) and
                        (self.tiles_collection[j].previous == None)):
                        previous_tile.next = self.tiles_collection[j]
                        self.tiles_collection[j].previous = previous_tile
                        previous_tile = self.tiles_collection[j]
                        pygame.draw.rect(self.screen, TILE_PATH_MARKER,
                                        pygame.Rect(self.tiles_collection[j].location[0],
                                        self.tiles_collection[j].location[1],
                                        9, 9), 2)


    def is_next_by_distance(self, tile1, tile2):
        compare_dist = int(self.base_size / ROW_COUNT)
        loc1 = tile1.location
        loc2 = tile2.location
        actual_dist = int(math.sqrt((loc1[0] - loc2[0])**2 + (loc1[1] -
                                                          loc2[1])**2))
        return compare_dist == actual_dist


    def create_board(self):
        row_inc = int((self.base_size / ROW_COUNT ) * 0.5)
        tile_num = 0
        half_board_count = math.floor(ROW_COUNT / 2) - 1
        for row in range(0, ROW_COUNT):
            if (row > half_board_count - 1 and row < half_board_count + 3):
                column_inc = int((self.base_size / ROW_COUNT) * 0.5)
                for column in range(0, ROW_COUNT):
                    if (column < half_board_count or column > half_board_count
                       + 2):
                        if (row == 7):
                            color = TILE_CENTER_COLOR
                            tile_type = 1
                            self.center_y = row_inc
                            if (column == 0) or (column == ROW_COUNT - 1):
                                is_path = True
                                color = TILE_START_COLOR
                            else:
                                is_path = False
                        else:
                            color = TILE_BOUNDARY_COLOR
                            tile_type = 0
                            is_path = True
                        new_tile = Tile(self.screen, TILE_SIZE, [column_inc,
                                        row_inc], color, 0, tile_type, is_path)
                        self.tiles_collection[tile_num] = new_tile
                        tile_num += 1
                    column_inc += int(self.base_size / ROW_COUNT)
            else:
                vertical_column_inc = int((self.base_size / ROW_COUNT) * 0.5)
                for column in range(0, ROW_COUNT):
                    if (column > half_board_count - 1 and column <
                        half_board_count + 3):
                        if column == 7:
                            color = TILE_CENTER_COLOR
                            tile_type = 1
                            self.center_x = vertical_column_inc
                            if (row == 0) or (row == ROW_COUNT - 1):
                                is_path = True
                                color = TILE_START_COLOR
                            else:
                                is_path = False
                        else:
                            color = TILE_BOUNDARY_COLOR
                            tile_type = 0
                            is_path = True
                        if (column == half_board_count and row == ROW_COUNT - 1):
                            color = TILE_START_COLOR
                            new_tile = Tile(self.screen, TILE_SIZE,
                                            [vertical_column_inc, row_inc], color,
                                            0, tile_type, is_path)
                            self.start_tile = new_tile
                        else:
                            new_tile = Tile(self.screen, TILE_SIZE,
                                            [vertical_column_inc, row_inc], color,
                                            0, tile_type, is_path)
                        self.tiles_collection[tile_num] = new_tile
                        tile_num += 1
                        if (column == 7) and ((row == half_board_count - 1) or \
                           (row == half_board_count + 3)):
                            decrement = int(self.base_size / ROW_COUNT)
                            new_tile = Tile(self.screen, TILE_SIZE,
                                        [vertical_column_inc - decrement * 2,
                                         row_inc], TILE_BOUNDARY_COLOR,
                                        0, 0, True)
                            self.tiles_collection[tile_num] = new_tile
                            tile_num += 1
                            new_tile = Tile(self.screen, TILE_SIZE,
                                        [vertical_column_inc + decrement * 2,
                                         row_inc], TILE_BOUNDARY_COLOR,
                                        0, 0, True)
                            self.tiles_collection[tile_num] = new_tile
                            tile_num += 1
                    vertical_column_inc += int(self.base_size / ROW_COUNT)
            row_inc += int(self.base_size / ROW_COUNT)


    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_SIZE[0],
                                               SCREEN_SIZE[1]))
        self.tiles_collection = {}
        self.start_tile = None
        self.center_x = 0
        self.center_y = 0
        self.base_size = min(SCREEN_SIZE)
        self.base_size -= TILE_SIZE
        self.create_board()
        self.post_processing()


class Ludo:
    pass


if __name__ == "__main__":
    board = Board()
    # for tile in tiles_dict:
    #     print(tiles_dict[tile].location)
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        pygame.display.flip()
        clock.tick(30)
