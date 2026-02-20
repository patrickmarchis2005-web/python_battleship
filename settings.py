from enum import Enum


class DifficultyType(Enum):
    EASY = 0
    HARD = 1


class Settings:
    __instance = None

    @staticmethod
    def get_instance():
        if Settings.__instance is not None:
            return Settings.__instance
        fin = open("settings.properties", "rt")
        file_lines = fin.readlines()
        fin.close()

        settings_dict = {}
        for line in file_lines:
            if line.strip().startswith("#"):
                continue
            tokens = line.strip().split("=")
            settings_dict[tokens[0].strip()] = tokens[1].strip()

        diff_type = settings_dict["difficulty"]

        difficulty_type =DifficultyType.EASY
        if diff_type == "hard":
            difficulty_type =DifficultyType.HARD

        Settings.__instance = Settings(difficulty_type)
        return Settings.__instance

    def __init__(self, difficulty_type):
        self.__difficulty_type = difficulty_type

    @property
    def difficulty_type(self):
        return self.__difficulty_type

