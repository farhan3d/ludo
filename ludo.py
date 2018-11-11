import math
import pygame
import random
import sys


SCREEN_SIZE = [600, 600]
ROW_COUNT = 15
TILE_BOUNDARY_COLOR = (0, 204, 204)
TILE_CENTER_COLOR = (255, 178, 102)
TILE_START_COLOR = (255, 255, 0)
TILE_PATH_MARKER = (255, 0, 255)
TILE_SIZE = math.floor(ROW_COUNT * 2.25)
PLAYER_RED = (204, 0, 0)
PLAYER_BLUE = (51, 51, 255)
PIECE_SIZE = 13
MOVE_SPEED = 40
DECELERATION = 0.25


pygame.init()
clock = pygame.time.Clock()
pygame.font.init()


class Player:

    def get_home_piece(self):
        home_piece = None
        for i in range(0, 4):
            if self.pieces[i].is_home:
                home_piece = self.pieces[i]
        return home_piece

    def get_farthest_piece(self):
        temp_pieces_arr = self.pieces[:]
        for i in range(0, 3):
            if (temp_pieces_arr[i].tiles_traversed >= \
               temp_pieces_arr[i+1].tiles_traversed) or \
               (temp_pieces_arr[i].is_home is False and \
                temp_pieces_arr[i+1].is_home is True):
                temp_pieces_arr[i], temp_pieces_arr[i+1] = \
                        temp_pieces_arr[i+1], temp_pieces_arr[i]
        if temp_pieces_arr[3].is_home is False:
            return temp_pieces_arr[3]
        else:
            return None

    """function should ideally return a piece based on player
    preference, but for now we will push the first piece found
    free in the list"""
    def get_free_piece(self):
        free_piece = None
        for i in range(0, 4):
            if self.pieces[i].is_home is False:
                free_piece = self.piece[i]
                break
        return free_piece

    def __init__(self, screen, color, name, location_set):
        self.player_name = name
        self.pieces = []
        self.location_set = location_set
        self.color = color
        for i in range(0, 4):
            self.pieces.append(Piece(screen, self, self.location_set[i], i + 1,
                                     PIECE_SIZE, color))


class Piece:

    def move_piece(self, screen):
        if self.target_tile or self.target_home_location:
            #print(pygame.time.get_ticks())
            target_location = None
            if self.target_home_location:
                target_location = self.target_home_location
            else:
                target_location = self.target_tile.location
            computed_vector = [target_location[0] - self.location[0],
                               target_location[1] - self.location[1]]
            vector_magnitude = math.sqrt(computed_vector[0]**2 +
                                         computed_vector[1]**2)
            computed_vector = [computed_vector[0] / vector_magnitude,
                               computed_vector[1] / vector_magnitude]
            current_distance = math.sqrt((target_location[0] -
                                          self.location[0])**2 +
                                         (target_location[1] -
                                          self.location[1])**2)
            self.current_move_speed = current_distance * DECELERATION
            """ Movement correction to avoid linear transitions """
            if current_distance < 10:
                self.location = [math.ceil(self.location[0] + computed_vector[0] *
                                 self.current_move_speed), math.ceil(self.location[1] +
                                 computed_vector[1] * self.current_move_speed)]
            if current_distance < 1:
                self.location = self.target_tile.location
            else:
                self.location = [self.location[0] + computed_vector[0] *
                                 self.current_move_speed, self.location[1] +
                                 computed_vector[1] * self.current_move_speed]
            self.current_move_speed *= DECELERATION
            self.draw_piece(screen)
            if self.target_home_location:
                if self.location == self.target_home_location:
                    self.target_home_location = None
                    self.current_tile = None
                    return True
                else:
                    return False
            else:
                if self.location == self.target_tile.location:
                    self.current_tile = self.target_tile
                    self.target_tile = None
                    return True
                else:
                    return False

    def draw_piece(self, screen):
        self.location = [int(self.location[0]), int(self.location[1])]
        circle = pygame.draw.circle(screen, self.color, self.location, self.size)
        return circle

    def __init__(self, screen, player, location, number, size, color):
        self.size = size
        self.current_tile = None
        self.location = location
        self.home_location = location
        self.target_tile = None
        self.target_home_location = None
        self.player = player
        self.color = color
        self.is_home = True
        self.tiles_traversed = 0
        self.current_move_speed = MOVE_SPEED


class Tile:

    def redraw_tile(self, screen):
        pygame.draw.rect(screen, self.color,
                         pygame.Rect(self.location_for_draw[0],
                                     self.location_for_draw[1], TILE_SIZE,
                                     TILE_SIZE), 2)

    def __init__(self, screen, size, location_arr, color, state, tile_type,
                 is_path=None):
        self.location_for_draw = location_arr
        self.location = [math.ceil(location_arr[0] + TILE_SIZE / 2),
                         math.ceil(location_arr[1] + TILE_SIZE / 2)]
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
        compare_dist = int(self.base_size / ROW_COUNT)
        loc1 = tile1.location
        loc2 = tile2.location
        actual_dist = int(math.sqrt((loc1[0] - loc2[0])**2 + (loc1[1] -
                                    loc2[1])**2))
        return compare_dist == actual_dist

    def redraw_pieces(self, player):
        for piece in player.pieces:
            piece.draw_piece(self.screen)

    def create_board_center_rows(self, row, row_inc, tile_num, half_board_count):
        column_inc = int((self.base_size / ROW_COUNT) * 0.5)
        for column in range(0, ROW_COUNT):
            if (column < half_board_count or column > half_board_count
                + 2):
                if (row == half_board_count + 1):
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
        return tile_num

    def create_board_center_columns(self, row, row_inc, tile_num, half_board_count):
        vertical_column_inc = int((self.base_size / ROW_COUNT) * 0.5)
        for column in range(0, ROW_COUNT):
            if (column > half_board_count - 1 and column <
                half_board_count + 3):
                if column == half_board_count + 1:
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
                new_tile = Tile(self.screen, TILE_SIZE,
                                [vertical_column_inc, row_inc], color,
                                0, tile_type, is_path)
                if (column == half_board_count and row == ROW_COUNT - 1):
                    self.start_tile = new_tile
                    self.start_tile_player1 = self.start_tile
                if (column == half_board_count + 2 and row == 0):
                    self.start_tile_player2 = new_tile
                self.tiles_collection[tile_num] = new_tile
                tile_num += 1
                if (column == half_board_count + 1) and \
                   ((row == half_board_count - 1) or
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
        return tile_num

    def create_board(self):
        row_inc = int((self.base_size / ROW_COUNT) * 0.5)
        tile_num = 0
        half_board_count = math.floor(ROW_COUNT / 2) - 1
        for row in range(0, ROW_COUNT):
            if (row > half_board_count - 1 and row < half_board_count + 3):
                tile_num = self.create_board_center_rows(row, row_inc, tile_num, half_board_count)
            else:
                tile_num = self.create_board_center_columns(row, row_inc, tile_num,
                                                 half_board_count)
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
        right_set.append([cell_size * ROW_COUNT - cell_size * 3,
                          cell_size * 2])
        right_set.append([cell_size * ROW_COUNT - cell_size, cell_size +
                          cell_size * 3])
        right_set.append([cell_size * ROW_COUNT - cell_size * 3, cell_size +
                          cell_size * 3])
        self.location_sets.append(right_set)

    def update_dice_text(self, text, color):
        self.dice_text_surf = self.dice_text.render(text, False, color)
        self.screen.blit(self.dice_text_surf, (SCREEN_SIZE[0] / 2 -
                                               TILE_SIZE / 1.75,
                                               SCREEN_SIZE[1] / 2 -
                                               TILE_SIZE))

    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_SIZE[0],
                                               SCREEN_SIZE[1]))
        self.tiles_collection = {}
        self.start_tile = None
        self.start_tile_player1 = None
        self.start_tile_player2 = None
        self.center_x = 0
        self.center_y = 0
        self.location_sets = []
        self.base_size = min(SCREEN_SIZE)
        self.base_size -= TILE_SIZE
        self.create_board()
        self.post_processing()
        self.calculate_home_location_sets()
        self.dice_text = pygame.font.SysFont('Arial', 72)
        self.dice_text_surf = self.dice_text.render('0', False, PLAYER_BLUE)


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
        self.current_player = self.player1
        self.current_piece = None
        self.turn_under_progress = False
        self.move_current_piece = False
        self.dice_num = 0
        self.game(board)

    def toggle_player(self):
        if self.current_player == self.player1:
            self.current_player = self.player2
        else:
            self.current_player = self.player1

    def increment_piece_target_tile(self, board, piece, increment):
        for i in range(0, increment):
            piece.target_tile = piece.current_tile.next
            piece.current_tile = piece.target_tile
        piece.tiles_traversed += increment

    def check_and_process_collision(self, attacker, victim):
        collision_count = 0
        victim_piece = None
        for attack_piece in attacker.pieces:
            for current_victim_piece in victim.pieces:
                if attack_piece.location == current_victim_piece.location:
                    victim_piece = current_victim_piece
                    collision_count += 1
        """ Only consider it valid attack if victim doesn't have two
        overlapping pieces at the same location """
        if collision_count == 1:
            victim_piece.is_home = True
            victim_piece.tiles_traversed = 0
            victim_piece.target_home_location = \
                    victim_piece.home_location
            self.current_piece = victim_piece
            return True
        else:
            return False

    def process_dice_throw(self):
        board.update_dice_text(str(self.dice_num), self.current_player.color)
        if self.dice_num == 6:
            player_home_piece = self.current_player.get_home_piece()
            if player_home_piece:
                self.current_piece = player_home_piece
                if self.current_player == self.player1:
                    self.current_piece.target_tile = board.start_tile_player1
                else:
                    self.current_piece.target_tile = board.start_tile_player2
                self.move_current_piece = True
            else:
                self.current_piece = self.current_player.get_farthest_piece()
                self.increment_piece_target_tile(board, self.current_piece,
                                                 self.dice_num)
                self.move_current_piece = True
        else:
            self.current_piece = self.current_player.get_farthest_piece()
            if self.current_piece:
                self.increment_piece_target_tile(board, self.current_piece,
                                                 self.dice_num)
                self.move_current_piece = True
            else:
                self.toggle_player()
                self.turn_under_progress = False

    def process_player_action(self):
        target_reached = self.current_piece.move_piece(board.screen)
        if target_reached is True:
            if (self.current_piece.location == board.start_tile_player1.location or
                self.current_piece.location == board.start_tile_player2.location):
                self.current_piece.is_home = False
                self.current_piece.tiles_traversed += 1
            if self.current_player == self.player1:
                other_player = self.player2
            else:
                other_player = self.player1
            if self.check_and_process_collision(self.current_player,
                                                other_player):
                pass
            else:
                self.move_current_piece = False
            self.turn_under_progress = False
            self.toggle_player()

    def game(self, board):
        done = False
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.KEYDOWN and self.move_current_piece is False:
                    if (event.key == pygame.K_SPACE and
                        self.turn_under_progress is False):
                        self.dice_num = self.roll_dice()
                        self.turn_under_progress = True
                    if (event.key == pygame.K_ESCAPE):
                        sys.exit()
            if self.turn_under_progress and self.move_current_piece is False:
                self.process_dice_throw()
            if self.move_current_piece:
                self.process_player_action()
            board.screen.fill((0, 0, 0))
            board.redraw_pieces(self.player1)
            board.redraw_pieces(self.player2)
            for tile_num in board.tiles_collection:
                tile = board.tiles_collection[tile_num]
                tile.redraw_tile(board.screen)
            board.screen.blit(board.dice_text_surf, (SCREEN_SIZE[0] / 2 -
                                                     TILE_SIZE / 1.75,
                                                     SCREEN_SIZE[1] / 2 -
                                                     TILE_SIZE))
            pygame.display.flip()
            clock.tick(60)


if __name__ == "__main__":
    board = Board()
    game = Ludo(board)

