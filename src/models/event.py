from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class Event:
    date: datetime
    title: str
    description: str
    program: str
