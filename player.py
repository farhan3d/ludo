import const
from piece import *

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
                                     const.PIECE_SIZE, color))
