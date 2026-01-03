import json
from pathlib import Path
from typing import Dict, Any


class QuizRepository:
    def __init__(self, quizzes_file: Path):
        self._quizzes_file = quizzes_file

    def save_quizzes(self, quizzes: Dict[str, Any]) -> None:
        data = self._load()

        data["quizzes"] = {
            quiz_name: {
                "questions": questions,
            }
            for quiz_name, questions in quizzes.items()
        }

        self._save(data)

    def get_quizzes(self) -> Dict[str, Any]:
        data = self._load()

        return {
            quiz_name: quiz_data.get("questions", [])
            for quiz_name, quiz_data in data.get("quizzes", {}).items()
        }

    def _load(self) -> dict:
        if not self._quizzes_file.exists():
            return {"quizzes": {}}

        with self._quizzes_file.open("r", encoding="utf-8") as f:
            return json.load(f)

    def _save(self, data: dict) -> None:
        self._quizzes_file.parent.mkdir(parents=True, exist_ok=True)

        with self._quizzes_file.open("w", encoding="utf-8") as f:
            json.dump(
                data,
                f,
                ensure_ascii=False,
                indent=2,
            )
