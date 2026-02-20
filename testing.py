import unittest


from board.board import *
from game.game import *


class TestPlaceShip(unittest.TestCase):
    def test_place_player_ship(self):
        pb = PlayerBoard()
        pb.place_ship(5,5,ShipDirection.DOWN,ShipType.CARRIER)
        line = [0,0,0,0,0,1,0,0,0,0]
        self.assertIn(line, pb.data)

    def test_place_computer_ship(self):
        cb = ComputerBoard()
        cb.place_ship(5,5,ShipDirection.DOWN,ShipType.CARRIER)
        line = [0,0,0,0,0,1,0,0,0,0]
        self.assertIn(line, cb.data)


class TestFireBoard(unittest.TestCase):
    def test_fire_player_board(self):
        pb = PlayerBoard()
        pb.place_ship(5,5,ShipDirection.DOWN,ShipType.CARRIER)
        try:
            pb.fire(0,0)
        except ShipSunkError:
            pass
        line = [100, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.assertIn(line,pb.data)

    def test_fire_computer_board(self):
        cb = ComputerBoard()
        cb.place_ship(5,5,ShipDirection.DOWN,ShipType.CARRIER)
        try:
            cb.fire(0,0)
        except ShipSunkError:
            pass
        line = [100, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.assertIn(line, cb.data)


class TestComputerStrategy(unittest.TestCase):
    def test_computer_place_ship(self):
        cb = ComputerBoard()
        pb = PlayerBoard()
        cs = ComputerStrategy(cb, pb)
        coordinates = cs.coordinates
        for i in range(1, 6):
            x,y = coordinates[i-1]
            value = cb.data[x][y]
            self.assertEqual(value, i)


if __name__ == '__main__':
    unittest.main()

