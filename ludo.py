import pygame


SCREEN_SIZE = [800, 600]


pygame.init()


class Player:
    pass


class Piece:
    pass


class Board:
    pass


class Tile:
    pass


class Ludo:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_SIZE[0], SCREEN_SIZE[1]))
        


if __name__ == "__main__":
    app = Ludo()
