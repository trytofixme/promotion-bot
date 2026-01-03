import asyncio
import json
from pathlib import Path


class UserRepository:
    def __init__(self, users_file: Path):
        self._users_file = users_file
        self._lock = asyncio.Lock()

    async def add_user(self, user_id: int) -> None:
        async with self._lock:
            users = self._load()
            if user_id not in users:
                users.add(user_id)
                self._save(users)

    def remove_user(self, user_id: int) -> None:
        users = self._load()
        if user_id in users:
            users.remove(user_id)
            self._save(users)

    def get_users(self) -> list[int]:
        return list(self._load())

    def _load(self) -> set[int]:
        if not self._users_file.exists():
            return set()

        with self._users_file.open("r", encoding="utf-8") as f:
            data = json.load(f)

        return set(data.get("users", []))

    def _save(self, users: set[int]) -> None:
        self._users_file.parent.mkdir(parents=True, exist_ok=True)

        with self._users_file.open("w", encoding="utf-8") as f:
            json.dump(
                {"users": list(users)},
                f,
                ensure_ascii=False,
                indent=2,
            )