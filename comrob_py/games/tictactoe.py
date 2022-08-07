"""
This file contains the logic for the tic-tac-toe Game.
"""
# TODO (ALR): Might be nice to have an interchangeable game class, tbd.
from enum import Enum
import random

from comrob_py.robot_handler.comrob_error import ComrobError, ErrorCode


class TicTacToe:
    """
    The TicTacToe class contains the logic for a classic tic-tac-toe game, where one player is artificial. The real
    player plays the cross, the artificial player plays circles.
    The field positions are numbered from 1-9, row wise:
    1 2 3
    4 5 6
    7 8 9
    """
    class Tile(Enum):
        """
        A Tile is either a cross, a circle, or empty, and represents the state of a tile on the tic-tac-toe playing field.
        Full is a condition for checking if the game has ended
        """
        Cross = "cross"
        Circle = "circle"
        Empty = "Empty"
        Full = "Full"

    def __init__(self):
        """
        Constructor.
        """
        self.__field = [self.Tile.Empty for i in range(9)]

    @property
    def field(self):
        """
        Getter for the status of the playing field.
        """
        return self.__field

    def update(self, tile_number):
        """
        Update the game with one player move and one artificial move.
        :param tile_number: tile position the player wants to cross (1-9)
        :type tile_number: int
        :return: the status of the game, whether it has ended (either cross won, circle won, of field is full) or is
        still ongoing (empty)
        :rtype: Tile
        """
        # TODO (ALR): Add an option for a random starting order.
        self.__player_move(tile_number)
        game_status = self.__check_game_end()
        if game_status != self.Tile.Empty:
            return game_status

        self.__artificial_move()
        return self.__check_game_end()

    def __player_move(self, tile_number):
        """
        :param tile_number: tile position the player wants to cross (1-9)
        :type tile_number: int
        """
        if self.__field[tile_number - 1] != self.Tile.Empty:
            raise ComrobError(ErrorCode.E0014, "Could not put a cross on that field, since it is already occupied.")

        self.__field[tile_number - 1] = self.Tile.Cross

    def __artificial_move(self):
        """
        Random artificial move placing one circle tile on the field.
        """
        # find empty positions
        empty_positions = []
        for i in range(9):
            if self.__field[i] == self.Tile.Empty:
                empty_positions.append(i)

        # select one at random
        position = random.randint(0, len(empty_positions) - 1)
        self.__field[position] = self.Tile.Circle

    def __check_game_end(self):
        """
        Check if the game ended, either by someone winning or the field being full.
        :return: Returns Cross or Circle if either won, returns Empty if no one won but there is still room, returns
        Full if the field is full but no one won.
        :rtype: Tile
        """
        # TODO (ALR): I'm sure there is a smarter solution for this.
        # first check if a player won with rows, columns or diagonals
        triplets = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [1, 4, 7], [2, 5, 8], [3, 6, 9], [1, 5, 9], [3, 5, 7]]
        for triplet in triplets:
            triplet_check = self.__check_triplet(triplet)
            if triplet_check != self.Tile.Empty:
                return triplet_check

        # check if all tiles are full but no one won
        for i in range(9):
            if self.__field[i] == self.Tile.Empty:
                return self.Tile.Empty

        return self.Tile.Full

    def __check_triplet(self, triplet):
        """
        Check if three places within the field have the same symbol.
        :param triplet: list containing the 3 positions to check, the 3 positions go from (1-9)
        :type triplet: list
        :return: Cross if three crosses, Circle if three circles, Empty otherwise
        :rtype: Tile
        """
        crosses = 0
        circles = 0
        for element in triplet:
            if self.__field[element - 1] == self.Tile.Cross:
                crosses += 1
            elif self.__field[element - 1] == self.Tile.Circle:
                circles += 1

        if crosses == 3:
            return self.Tile.Cross
        elif circles == 3:
            return self.Tile.Circle

        return self.Tile.Empty

