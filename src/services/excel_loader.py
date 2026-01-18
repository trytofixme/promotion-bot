from collections import defaultdict
from typing import List, Dict, Any

import pandas as pd

from src.models.event import Event


class ExcelLoader:
    REQUIRED_QUIZ_COLUMNS = {"Викторина", "Вопрос", "Ответ", "Правильный ответ"}

    def load_events(self, file) -> List[Event]:
        df = pd.read_excel(file)

        events: List[Event] = []

        for _, row in df.iterrows():
            events.append(
                Event(
                    date=pd.to_datetime(row["Дата"]).to_pydatetime(),
                    title=str(row["Название"]).strip(),
                    description=str(row["Описание"]).strip(),
                    program=str(row["Программа"]).strip(),
                )
            )

        return events

    def load_quizzes(self, file) -> Dict[str, List[Dict[str, Any]]]:
        df = pd.read_excel(file)
        self._validate_quiz_columns(df)

        quizzes = defaultdict(lambda: defaultdict(list))

        for _, row in df.iterrows():
            quiz = str(row["Викторина"]).strip()
            question = str(row["Вопрос"]).strip()
            answer = str(row["Ответ"]).strip()
            is_correct = str(row["Правильный ответ"])

            quizzes[quiz][question].append(
                {
                    "text": answer,
                    "correct": is_correct,
                }
            )

        return self._to_result(quizzes)

    @classmethod
    def _validate_quiz_columns(cls, df: pd.DataFrame) -> None:
        if not cls.REQUIRED_QUIZ_COLUMNS.issubset(df.columns):
            missing = cls.REQUIRED_QUIZ_COLUMNS - set(df.columns)
            raise ValueError(
                f"Excel должен содержать колонки: {', '.join(missing)}"
            )

    @staticmethod
    def _to_result(
        quizzes: Dict[str, Dict[str, List[Dict[str, Any]]]]
    ) -> Dict[str, List[Dict[str, Any]]]:
        result = {}

        for quiz, questions in quizzes.items():
            result[quiz] = []
            for question, answers in questions.items():
                result[quiz].append(
                    {
                        "question": question,
                        "answers": answers,
                    }
                )

        return result
