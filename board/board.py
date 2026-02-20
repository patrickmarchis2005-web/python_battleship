from enum import Enum


from texttable import Texttable


class OverlapError(Exception):
    pass


class OutsideBoardError(Exception):
    pass


class ShipSunkError(Exception):
    def __init__(self, nr: int = 0) -> None:
        self.__nr = nr

    def __str__(self) -> str:
        return "You sank " + str(self.__nr) + " ship(s)!"

    def nr(self) -> int:
        return int(self.__nr)


class AllSunkError(Exception):
    pass


class ShipDirection(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


class ShipType(Enum):
    CARRIER = 0
    BATTLESHIP = 1
    CRUISER = 2
    SUBMARINE = 3
    DESTROYER = 4


class BattleshipsBoard:
    # The rules are not tied to any single board, so they don't need the self parameter
    # this is a general placement rule
    # These are class-level variables (similar to static variables in other languages)
    __placement_rules = {ShipDirection.UP: (-1, 0), ShipDirection.DOWN: (1, 0), ShipDirection.LEFT: (0, -1),
                         ShipDirection.RIGHT: (0, 1)}

    __ship_length = {ShipType.CARRIER: 5, ShipType.BATTLESHIP: 4, ShipType.CRUISER: 3, ShipType.SUBMARINE: 3, ShipType.DESTROYER: 2}

    def __init__(self):
        self._data = []
        for i in range(10):
            self._data.append([0] * 10)
        # we represent the next added ship using 1's
        self.__current_ship = 1

    def place_ship(self, row: int, column: int, direction: ShipDirection, type: ShipType):
        """
        Places a ship on the board
        :param row: the row where the ship will be placed
        :param column: the column where the ship will be placed
        :param direction: the direction where the ship will be placed
        :param type: the type of the ship
        :return:
        """
        move_x = BattleshipsBoard.__placement_rules[direction][0]
        move_y = BattleshipsBoard.__placement_rules[direction][1]
        fake_x = row
        fake_y = column
        current_x = row
        current_y = column

        # here I check if a ship is contained in the board and if it doesn't overlap other ship
        for cell in range(0, BattleshipsBoard.__ship_length[type]):
            if fake_x < 0 or fake_x > 9 or fake_y < 0 or fake_y > 9:
                raise OutsideBoardError
            elif self._data[fake_x][fake_y] != 0:
                raise OverlapError
            fake_x += move_x
            fake_y += move_y

        for cell in range(0, BattleshipsBoard.__ship_length[type]):
            self._data[current_x][current_y] = self.__current_ship
            current_x += move_x
            current_y += move_y
        # move to the next ship index
        self.__current_ship += 1
        return row, column

    def fire(self, row: int, column: int):
        """
        Fires a cell on the board (hopefully a ship)
        :param row: the row of the cell to be fired
        :param column: the column of the cell to be fired
        :return:
        """
        if self._data[row][column] == 0:
            self._data[row][column] = 100
        elif self._data[row][column] < 0:
            raise ValueError # the player chose a cell already shot
        elif self._data[row][column] > 0 and self._data[row][column] != 100:
            self._data[row][column] = -1 * self._data[row][column]

        sunk = True # False = no ship sunk
        ships_sunk = 0
        for token in range(1, 6):
            for i in range(10):
                for j in range(10):
                    if self._data[i][j] == token:
                        sunk = False
            if sunk:
                ships_sunk += 1
            sunk = True
        if ships_sunk == 5:
            raise AllSunkError # means all the ships are sunk, which means the game is over
        elif ships_sunk != 0:
            raise ShipSunkError(ships_sunk) # means at least one ship is sunk

    @property
    def data(self):
        return self._data


class PlayerBoard(BattleshipsBoard):
    def __init__(self):
        super().__init__()

    def __str__(self):
        """
        Here I manage how the player's board will look
        :return:
        """
        t = Texttable()
        t.header(['\\', 'A ', 'B ', 'C ', 'D ', 'E ', 'F ', 'G ', 'H ', 'I ', 'J '])  # easier with ord(), chr()
        # for ascii_code in range(ord('A'),ord('F')+1):
        #     print(chr(ascii_code))
        for row in range(10):
            row_data = [row + 1] + [' '] * 10  # initialize an empty row
            for column in range(10):
                symbol = ' '
                if self._data[row][column] == 100:
                    symbol = '.'
                elif self._data[row][column] > 0:
                    symbol = str(self._data[row][column])
                elif self._data[row][column] < 0:
                    symbol = 'X'
                row_data[column + 1] = symbol
            t.add_row(row_data)
        return t.draw()


class ComputerBoard(BattleshipsBoard):
    def __init__(self):
        super().__init__()

    def __str__(self):
        """
        Here I manage how the computer's board will look'
        :return:
        """
        t = Texttable()
        t.header(['\\', 'A ', 'B ', 'C ', 'D ', 'E ', 'F ', 'G ', 'H ', 'I ', 'J '])  # easier with ord(), chr()
        # for ascii_code in range(ord('A'),ord('F')+1):
        #     print(chr(ascii_code))
        for row in range(10):
            row_data = [row + 1] + [' '] * 10  # initialize an empty row
            for column in range(10):
                symbol = ' '
                if self._data[row][column] == 100:
                    symbol = '.'
                elif self._data[row][column] > 0:
                    symbol = str(self._data[row][column])
                elif self._data[row][column] < 0:
                    symbol = 'X'
                row_data[column + 1] = symbol
            t.add_row(row_data)
        return t.draw()


if __name__ == "__main__":
    bb = PlayerBoard()
    print(bb)
    bb.place_ship(0, 9, ShipDirection.UP, ShipType.CARRIER)
    # bb.place_ship(1, 2, ShipDirection.RIGHT, ShipType.CRUISER)
    # bb.place_ship(5, 5, ShipDirection.UP, ShipType.BATTLESHIP)
    # bb.fire(2, 1)
    # bb.fire(3, 3)
    print(bb)