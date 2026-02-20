from game.game import Battleships
from settings import Settings, DifficultyType
from ui.ui import UI

difficulty = None

if Settings.get_instance().difficulty_type == DifficultyType.EASY:
    difficulty = DifficultyType.EASY
elif Settings.get_instance().difficulty_type == DifficultyType.HARD:
    difficulty = DifficultyType.HARD

ui = UI(difficulty)
ui.start()

