import math
import pygame
import random
import sys
from player import *
from const import *
from board import *


pygame.init()
clock = pygame.time.Clock()
pygame.font.init()


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

