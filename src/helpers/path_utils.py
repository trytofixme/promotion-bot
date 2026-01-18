import sys
from pathlib import Path


class PathUtils:
    @staticmethod
    def data_root() -> Path:
        if getattr(sys, "frozen", False):
            return Path(sys.executable).parent / "data"
        else:
            return Path(__file__).resolve().parents[2] / "data"

    @classmethod
    def get_users_path(cls) -> Path:
        return cls.data_root() / "users.json"

    @classmethod
    def get_events_path(cls) -> Path:
        return cls.data_root() / "events.json"

    @classmethod
    def get_sended_events_path(cls) -> Path:
        return cls.data_root() / "sended_events.json"

    @classmethod
    def get_quizzes_path(cls) -> Path:
        return cls.data_root() / "quizzes.json"

    @classmethod
    def get_passed_quizzes_path(cls) -> Path:
        return cls.data_root() / "passed_quizzes.json"