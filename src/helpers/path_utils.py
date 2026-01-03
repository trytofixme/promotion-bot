from pathlib import Path


class PathUtils:
    @staticmethod
    def get_users_path() -> Path:
        return Path("../data/users.json")

    @staticmethod
    def get_events_path() -> Path:
        return Path("../data/events.json")

    @staticmethod
    def get_sended_events_path() -> Path:
        return Path("../data/sended_events.json")

    @staticmethod
    def get_quizzes_path() -> Path:
        return Path("../data/quizzes.json")

    @staticmethod
    def get_passed_quizzes_path() -> Path:
        return Path("../data/passed_quizzes.json")