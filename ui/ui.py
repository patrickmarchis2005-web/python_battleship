from board.board import ShipDirection, ShipType, OutsideBoardError, OverlapError, ShipSunkError, AllSunkError

from game.game import Battleships


class UI:
    def __init__(self, difficulty_type):
        self.__game = Battleships(difficulty_type)

    def __place_player_ships(self):
        for ship_type in ShipType:
            while True:
                print(self.__game.player_board)
                try:
                    # print("Coordinates for the " + str(ship_type) + ":")
                    # x = int(input("Enter X:"))
                    # y = int(input("Enter Y:"))
                    xy_coordinates = input("Coordinates for the " + str(ship_type) + ":").split(",")
                    if len(xy_coordinates[0]) > 1:
                        raise ValueError("Please enter a 'comma' between the coordinates!")
                    elif xy_coordinates[0] == "" or xy_coordinates[1] == "":
                        raise ValueError
                    if ord(xy_coordinates[0]) >= ord('a') or ord(xy_coordinates[0]) <= ord('j'):
                        xy_coordinates[0] = xy_coordinates[0].upper()
                    if ord(xy_coordinates[0]) < ord('A') or ord(xy_coordinates[0]) > ord('J'):
                        raise ValueError("Invalid coordinates")
                    elif not xy_coordinates[1].isdigit():
                        raise ValueError("Invalid coordinates. Should be: letter, nr")

                    direction = input("Enter Ship Direction:")
                    if direction == "left":
                        ship_direction = ShipDirection.LEFT
                    elif direction == "right":
                        ship_direction = ShipDirection.RIGHT
                    elif direction == "up":
                        ship_direction = ShipDirection.UP
                    elif direction == "down":
                        ship_direction = ShipDirection.DOWN
                    else:
                        raise ValueError("Direction must be 'left' or 'right' or 'up' or 'down'")
                    xy_coordinates[0] = ord(xy_coordinates[0]) - ord('A')
                    xy_coordinates[1] = int(xy_coordinates[1]) - 1
                    self.__game.player_board.place_ship(xy_coordinates[1], xy_coordinates[0], ship_direction, ship_type)
                    break
                except ValueError as ve:
                    # print("Invalid input. Please try again.")
                    print(ve)
                except OutsideBoardError:
                    print("The coordinates you entered are out of bounds. Please try again.")
                except OverlapError:
                    print("The coordinates you entered overwrite other ships. Please try again.")

    def start(self):
        # print(self.__game.player_board)
        self.__place_player_ships()
        while True:
            print("My board")
            print(self.__game.player_board)
            print("\nTargeting board")
            print(self.__game.computer_board)
            while True:
                try:
                    fire_coordinates = input("fire>").split(",")
                    if ord(fire_coordinates[0]) >= ord('a') or ord(fire_coordinates[0]) <= ord('j'):
                        fire_coordinates[0] = fire_coordinates[0].upper()
                    if ord(fire_coordinates[0]) < ord('A') or ord(fire_coordinates[0]) > ord('J'):
                        raise ValueError("Invalid coordinates")
                    elif not fire_coordinates[1].isdigit():
                        raise ValueError("Invalid coordinates")

                    column = ord(fire_coordinates[0].upper()) - ord('A')
                    row = int(fire_coordinates[1]) - 1
                    self.__game.fire_human_player(row, column)
                    break
                except ValueError:
                    print("Invalid coordinates, or a cell was shot twice or more. Please try again.")
                except ShipSunkError as sse:
                    print(sse)
                    break
                except AllSunkError:
                    print("\nYOU WON!\n")
                    return
            try:
                self.__game.fire_computer_player()
            except ShipSunkError:
                pass
            except AllSunkError:
                print("\nYOU LOST!\n")
                return



if __name__ == "__main__":
    # ui = UI()
    # ui.start()
    pass

