import const
import math
import pygame
from tile import *

class Board:

    """iterate over tiles and link them with each other in order of
    traversal"""
    def post_processing(self):
        previous_tile = None
        for i in range(len(self.tiles_collection)):
            if (self.is_next_by_distance(self.tiles_collection[i],
                self.start_tile) and (self.tiles_collection[i].type == 0)):
                self.start_tile.next = self.tiles_collection[i]
                self.tiles_collection[i].previous = self.start_tile
                previous_tile = self.tiles_collection[i]
        tile_counter = 0
        if previous_tile is not None:
            for k in range(len(self.tiles_collection)):
                for j in range(len(self.tiles_collection)):
                    if (self.is_next_by_distance(self.tiles_collection[j],
                        previous_tile) and (self.tiles_collection[j].is_path is True) and
                        (self.tiles_collection[j].next is None) and
                        (self.tiles_collection[j].previous is None)):
                        previous_tile.next = self.tiles_collection[j]
                        self.tiles_collection[j].previous = previous_tile
                        previous_tile = self.tiles_collection[j]
                        tile_counter += 1
        previous_tile.next = self.start_tile

    def is_next_by_distance(self, tile1, tile2):
        compare_dist = int(self.base_size / const.ROW_COUNT)
        loc1 = tile1.location
        loc2 = tile2.location
        actual_dist = int(math.sqrt((loc1[0] - loc2[0])**2 + (loc1[1] -
                                    loc2[1])**2))
        return compare_dist == actual_dist

    def redraw_pieces(self, player):
        for piece in player.pieces:
            piece.draw_piece(self.screen)

    def create_board_center_rows(self, row, row_inc, tile_num, half_board_count):
        column_inc = int((self.base_size / const.ROW_COUNT) * 0.5)
        for column in range(0, const.ROW_COUNT):
            if (column < half_board_count or column > half_board_count
                + 2):
                if (row == half_board_count + 1):
                    color = const.TILE_CENTER_COLOR
                    tile_type = 1
                    self.center_y = row_inc
                    if (column == 0) or (column == const.ROW_COUNT - 1):
                        is_path = True
                        color = const.TILE_START_COLOR
                    else:
                        is_path = False
                else:
                    color = const.TILE_BOUNDARY_COLOR
                    tile_type = 0
                    is_path = True
                new_tile = Tile(self.screen, const.TILE_SIZE, [column_inc,
                                row_inc], color, 0, tile_type, is_path)
                self.tiles_collection[tile_num] = new_tile
                tile_num += 1
            column_inc += int(self.base_size / const.ROW_COUNT)
        return tile_num

    def create_board_center_columns(self, row, row_inc, tile_num, half_board_count):
        vertical_column_inc = int((self.base_size / const.ROW_COUNT) * 0.5)
        for column in range(0, const.ROW_COUNT):
            if (column > half_board_count - 1 and column <
                half_board_count + 3):
                if column == half_board_count + 1:
                    color = const.TILE_CENTER_COLOR
                    tile_type = 1
                    self.center_x = vertical_column_inc
                    if (row == 0) or (row == const.ROW_COUNT - 1):
                        is_path = True
                        color = const.TILE_START_COLOR
                    else:
                        is_path = False
                else:
                    color = const.TILE_BOUNDARY_COLOR
                    tile_type = 0
                    is_path = True
                new_tile = Tile(self.screen, const.TILE_SIZE,
                                [vertical_column_inc, row_inc], color,
                                0, tile_type, is_path)
                if (column == half_board_count and row == const.ROW_COUNT - 1):
                    self.start_tile = new_tile
                    self.start_tile_player1 = self.start_tile
                if (column == half_board_count + 2 and row == 0):
                    self.start_tile_player2 = new_tile
                self.tiles_collection[tile_num] = new_tile
                tile_num += 1
                if (column == half_board_count + 1) and \
                   ((row == half_board_count - 1) or
                   (row == half_board_count + 3)):
                    decrement = int(self.base_size / const.ROW_COUNT)
                    new_tile = Tile(self.screen, const.TILE_SIZE,
                                    [vertical_column_inc - decrement * 2,
                                     row_inc], const.TILE_BOUNDARY_COLOR,
                                    0, 0, True)
                    self.tiles_collection[tile_num] = new_tile
                    tile_num += 1
                    new_tile = Tile(self.screen, const.TILE_SIZE,
                                [vertical_column_inc + decrement * 2,
                                 row_inc], const.TILE_BOUNDARY_COLOR,
                                0, 0, True)
                    self.tiles_collection[tile_num] = new_tile
                    tile_num += 1
            vertical_column_inc += int(self.base_size / const.ROW_COUNT)
        return tile_num

    def create_board(self):
        row_inc = int((self.base_size / const.ROW_COUNT) * 0.5)
        tile_num = 0
        half_board_count = math.floor(const.ROW_COUNT / 2) - 1
        for row in range(0, const.ROW_COUNT):
            if (row > half_board_count - 1 and row < half_board_count + 3):
                tile_num = self.create_board_center_rows(row, row_inc, tile_num, half_board_count)
            else:
                tile_num = self.create_board_center_columns(row, row_inc, tile_num,
                                                 half_board_count)
            row_inc += int(self.base_size / const.ROW_COUNT)

    def calculate_home_location_sets(self):
        left_set = []
        cell_size = int(self.base_size / const.ROW_COUNT)
        left_set.append([cell_size * 2, cell_size * const.ROW_COUNT - cell_size])
        left_set.append([cell_size * 4, cell_size * const.ROW_COUNT - cell_size])
        left_set.append([cell_size * 4, cell_size * const.ROW_COUNT - cell_size * 3])
        left_set.append([cell_size * 2, cell_size * const.ROW_COUNT - cell_size * 3])
        self.location_sets.append(left_set)
        right_set = []
        right_set.append([cell_size * const.ROW_COUNT - cell_size, cell_size * 2])
        right_set.append([cell_size * const.ROW_COUNT - cell_size * 3,
                          cell_size * 2])
        right_set.append([cell_size * const.ROW_COUNT - cell_size, cell_size +
                          cell_size * 3])
        right_set.append([cell_size * const.ROW_COUNT - cell_size * 3, cell_size +
                          cell_size * 3])
        self.location_sets.append(right_set)

    def update_dice_text(self, text, color):
        self.dice_text_surf = self.dice_text.render(text, False, color)
        self.screen.blit(self.dice_text_surf, (const.SCREEN_SIZE[0] / 2 -
                                               const.TILE_SIZE / 1.75,
                                               const.SCREEN_SIZE[1] / 2 -
                                               const.TILE_SIZE))

    def __init__(self):
        self.screen = pygame.display.set_mode((const.SCREEN_SIZE[0],
                                               const.SCREEN_SIZE[1]))
        self.tiles_collection = {}
        self.start_tile = None
        self.start_tile_player1 = None
        self.start_tile_player2 = None
        self.center_x = 0
        self.center_y = 0
        self.location_sets = []
        self.base_size = min(const.SCREEN_SIZE)
        self.base_size -= const.TILE_SIZE
        self.create_board()
        self.post_processing()
        self.calculate_home_location_sets()
        self.dice_text = pygame.font.SysFont('Arial', 72)
        self.dice_text_surf = self.dice_text.render('0', False, const.PLAYER_BLUE)
