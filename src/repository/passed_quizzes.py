import asyncio
import json
from pathlib import Path
from typing import Dict, Set

class QuizPassedRepository:
    def __init__(self, path: Path):
        self._path = path
        self._lock = asyncio.Lock()

    def _load(self) -> Dict[str, Set[int]]:
        if not self._path.exists():
            return {}

        with self._path.open("r", encoding="utf-8") as f:
            raw = json.load(f)

        quizzes = raw.get("quizzes", {})
        return {
            quiz_name: set(data.get("passed_users", []))
            for quiz_name, data in quizzes.items()
        }

    def _save(self, data: Dict[str, Set[int]]):
        self._path.parent.mkdir(parents=True, exist_ok=True)

        serializable = {
            "quizzes": {
                quiz: {
                    "passed_users": list(users)
                }
                for quiz, users in data.items()
            }
        }

        with self._path.open("w", encoding="utf-8") as f:
            json.dump(
                serializable,
                f,
                ensure_ascii=False,
                indent=2,
            )

    async def mark_passed(self, quiz_name: str, user_id: int):
        async with self._lock:
            data = self._load()
            users = data.setdefault(quiz_name, set())

            if user_id not in users:
                users.add(user_id)
                self._save(data)

    async def has_passed(self, quiz_name: str, user_id: int) -> bool:
        async with self._lock:
            data = self._load()
            return user_id in data.get(quiz_name, set())

    async def get_passed_users(self, quiz_name: str) -> list[int]:
        async with self._lock:
            data = self._load()
            return list(data.get(quiz_name, set()))
