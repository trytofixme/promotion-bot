import json
from datetime import datetime
from pathlib import Path
from typing import List

from src.models.event import Event

DATE_FMT = "%Y-%m-%d %H:%M:%S"


class EventRepository:
    def __init__(self, path: Path):
        self._path = path

    def get_events(self) -> List[Event]:
        data = self._load()
        return [self._dict_to_event(e) for e in data["events"]]

    def save_events(self, events: List[Event]):
        data = self._load()

        for event in events:
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
            "description": event.description,
            "program": event.program,
            "date": event.date.strftime(DATE_FMT),
        }

    @staticmethod
    def _dict_to_event(d: dict) -> Event:
        return Event(
            title=d["title"],
            description=d["description"],
            program=d["program"],
            date=datetime.strptime(d["date"], DATE_FMT),
        )
