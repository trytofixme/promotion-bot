import json
from datetime import datetime
from pathlib import Path

from src.models.event import Event

DATE_FMT = "%Y-%m-%d %H:%M:%S"


class SendedEventRepository:
    def __init__(self, path: Path):
        self._path = path

    def is_sended(self, event: Event) -> bool:
        data = self._load()
        return self._event_key(event) in {
            self._event_key_from_dict(e) for e in data["events"]
        }

    def mark_as_sended(self, event: Event):
        data = self._load()
        key = self._event_key(event)

        existing = {
            self._event_key_from_dict(e) for e in data["events"]
        }

        if key not in existing:
            data["events"].append(self._event_to_dict(event))
            self._save(data)

    def _load(self) -> dict:
        if not self._path.exists():
            return {"events": []}

        with self._path.open("r", encoding="utf-8") as f:
            return json.load(f)

    def _save(self, data: dict):
        self._path.parent.mkdir(parents=True, exist_ok=True)
        with self._path.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    @staticmethod
    def _event_to_dict(event: Event) -> dict:
        return {
            "title": event.title,
            "date": event.date.strftime(DATE_FMT),
        }

    @staticmethod
    def _event_key(event: Event) -> str:
        return f"{event.title}|{event.date.isoformat()}"

    @staticmethod
    def _event_key_from_dict(d: dict) -> str:
        date = datetime.strptime(d["date"], DATE_FMT).isoformat()
        return f"{d['title']}|{date}"
