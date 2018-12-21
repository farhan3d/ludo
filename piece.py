import const
import math
import pygame

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
            self.current_move_speed = current_distance * const.DECELERATION
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
            self.current_move_speed *= const.DECELERATION
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
        self.current_move_speed = const.MOVE_SPEED
