import math
import pygame
import random


SCREEN_SIZE = [600, 600]                    # the base canvas size
ROW_COUNT = 15                              # board size adjusts to this value
TILE_BOUNDARY_COLOR = (0, 204, 204)         # color of main movement tiles
TILE_CENTER_COLOR = (255, 178, 102)         # color of the safe zone center tiles
TILE_START_COLOR = (255, 255, 0)            # color of the start tile in tiles linked list
TILE_PATH_MARKER = (255, 0, 255)            # marker color for path tiles
TILE_SIZE = math.floor(ROW_COUNT * 2.25)    # a tile size adjusted from board size
PLAYER_RED = (204, 0, 0)
PLAYER_BLUE = (51, 51, 255)
MOVE_SPEED = 5
done = False                                # simple little bool to manage game loop


pygame.init()
clock = pygame.time.Clock()


class Player:

    def get_home_piece(self):
        home_piece = None
        for i in range(0, 4):
            if self.pieces[i].is_home:
                home_piece = self.piece[i]
        return home_piece

    """function should ideally return a piece based on player
    preference, but for now we will push the first piece found
    free in the list"""
    def get_free_piece():
        free_piece = None
        for i in range(0, 4):
            if self.pieces[i].is_home == False:
                free_piece = self.piece[i]
        return free_piece

    def __init__(self, screen, color, name, location_set):
        self.player_name = name
        self.pieces = []
        self.location_set = location_set
        for i in range(0, 4):
            self.pieces.append(Piece(screen, self, self.location_set[i], i + 1,
                                     10, color))


class Piece:

    def move_piece(self, destination_tile):
        pass

    def draw_piece(self, screen):
        pygame.draw.circle(screen, self.color, self.location, self.size)

    def __init__(self, screen, player, location, number, size, color):
        self.id = number
        self.size = size
        self.current_tile = None
        self.location = location
        self.home_location = location
        self.player = player
        self.color = color
        self.is_home = True
        self.draw_piece(screen)


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


    def is_next_by_distance(self, tile1, tile2):
        compare_dist = int(self.base_size / ROW_COUNT)
        loc1 = tile1.location
        loc2 = tile2.location
        actual_dist = int(math.sqrt((loc1[0] - loc2[0])**2 + (loc1[1] -
                                    loc2[1])**2))
        return compare_dist == actual_dist


    def create_board(self):
        row_inc = int((self.base_size / ROW_COUNT) * 0.5)
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

    def calculate_home_location_sets(self):
        left_set = []
        cell_size = int(self.base_size / ROW_COUNT)
        left_set.append([cell_size * 2, cell_size * ROW_COUNT - cell_size])
        left_set.append([cell_size * 4, cell_size * ROW_COUNT - cell_size])
        left_set.append([cell_size * 4, cell_size * ROW_COUNT - cell_size * 3])
        left_set.append([cell_size * 2, cell_size * ROW_COUNT - cell_size * 3])
        self.location_sets.append(left_set)
        right_set = []
        right_set.append([cell_size * ROW_COUNT - cell_size, cell_size * 2])
        right_set.append([cell_size * ROW_COUNT - cell_size * 3, cell_size * 2])
        right_set.append([cell_size * ROW_COUNT - cell_size, cell_size + cell_size * 3])
        right_set.append([cell_size * ROW_COUNT - cell_size * 3, cell_size + cell_size * 3])
        self.location_sets.append(right_set)


    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_SIZE[0],
                                               SCREEN_SIZE[1]))
        self.tiles_collection = {}
        self.start_tile = None
        self.center_x = 0
        self.center_y = 0
        self.location_sets = []
        self.base_size = min(SCREEN_SIZE)
        self.base_size -= TILE_SIZE
        self.create_board()
        self.post_processing()
        self.calculate_home_location_sets()


class Ludo:

    def roll_dice(self):
        random.shuffle(self.dice)
        return self.dice[0]

    def __init__(self, board):
        self.dice = [1, 2, 3, 4, 5, 6]
        self.player1 = Player(board.screen, PLAYER_BLUE, 'player1',
                              board.location_sets[0])
        self.player2 = Player(board.screen, PLAYER_RED, 'player2',
                              board.location_sets[1])


if __name__ == "__main__":
    board = Board()
    game = Ludo(board)
    current_player = game.player1
    turn_under_progress = False
    dice_num = 0
    move_current_piece = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_SPACE and
                    turn_under_progress == False):
                    dice_num = game.roll_dice()
                    turn_under_progress = True
        if turn_under_progress:
            if dice_num == 6:
                pass
        if move_current_piece:
            pass

        pygame.display.flip()
        clock.tick(30)
