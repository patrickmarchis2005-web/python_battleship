from random import randint


from board.board import ComputerBoard, PlayerBoard, ShipDirection, OverlapError, ShipType, OutsideBoardError, \
    AllSunkError, ShipSunkError
from settings import DifficultyType


class ComputerStrategy:

    def __init__(self, computer_board: ComputerBoard, player_board: PlayerBoard):
        self.__computer_board = computer_board
        self.__player_board = player_board
        # NOTE the computer can already place its ships at this point
        coordinates = self.place_ships()
        self.__coordinates = coordinates
        self.__round = 1

    def place_ships(self):
        """
        Computer's strategy for placing ships on its own board
        :return: the coordinates of the placed ships
        """
        coordinates = []
        for ship_type in ShipType:
            while True:
                x = randint(0,10)
                y = randint(0,10)
                random_nr = randint(0, 3)
                direction = ShipDirection(random_nr)
                try:
                    (x, y) = self.__computer_board.place_ship(x, y, direction, ship_type)
                    coordinates.append((x, y))
                    break
                except OverlapError:
                    pass
                except OutsideBoardError:
                    pass
        return coordinates

    def fire_hard(self) -> tuple:
        """
        Computer's efficient strategy to fire
        """
        if self.__round <= 4:
            while True:
                row = randint(0, 9)
                column = randint(0, 9)
                try:
                    self.__player_board.fire(row, column)
                    break
                except ValueError: # this appears when the same cell is shot twice or more times
                    pass
                except AllSunkError:
                    raise AllSunkError
                except ShipSunkError:
                    raise ShipSunkError
            self.__round += 1
            return row, column

        elif self.__round == 5:
            for i in range(10):
                for j in range(10):
                    if self.__player_board.data[i][j] > 0 or self.__player_board.data[i][j] < 6:
                        try:
                            self.__player_board.fire(i, j)
                            self.__round = 1
                            return i, j
                        except ValueError:
                            pass
                        except AllSunkError:
                            raise AllSunkError
                        except ShipSunkError:
                            raise ShipSunkError

    def fire_easy(self) -> tuple:
        """
        Computer's inefficient strategy to fire
        :return:
        """
        while True:
            try:
                row = randint(0, 9)
                column = randint(0, 9)
                self.__player_board.fire(row, column)
                break
            except ValueError:
                pass
            except AllSunkError:
                raise AllSunkError
            except ShipSunkError:
                raise ShipSunkError
        return row, column

    @property
    def coordinates(self):
        return self.__coordinates


class Battleships:
    def __init__(self, difficulty_type):
        self.__computer_board = ComputerBoard()
        self.__player_board = PlayerBoard()
        self.__difficulty_type = difficulty_type
        self.__strategy = ComputerStrategy(self.__computer_board, self.__player_board)

    @property
    def computer_board(self):
        return self.__computer_board

    @property
    def player_board(self):
        return self.__player_board

    def fire_human_player(self, row: int, column: int):
        """
        Function that fires/shoots a cell on the other board, that the player wants
        :param row: the row from the computer's board that is fired/shot
        :param column: the column from the computer's board that is fired/shot
        :return:
        """
        try:
            self.__computer_board.fire(row, column)
        except ValueError:
            raise ValueError
        except AllSunkError:
            raise AllSunkError
        except ShipSunkError:
            raise ShipSunkError

    def fire_computer_player(self):
        """
        Function that fires/shoots a cell on the other board, that the computer computes
        :return:
        """
        if self.__difficulty_type == DifficultyType.EASY:
            try:
                self.__strategy.fire_easy()
            except AllSunkError:
                raise AllSunkError
            except ShipSunkError:
                raise ShipSunkError

        elif self.__difficulty_type == DifficultyType.HARD:
            try:
                self.__strategy.fire_hard()
            except AllSunkError:
                raise AllSunkError
            except ShipSunkError:
                raise ShipSunkError

