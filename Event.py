"""
Описывает некоторе "событие" - промежуток времени с присвоенными характеристиками
У события должно быть описание, название и список участников
Событие может быть единожды созданым
Или периодическим (каждый день/месяц/год/неделю)

Каждый пользователь ивента имеет свою "роль"
организатор умеет изменять названия, список участников, описание, а так же может удалить событие
участник может покинуть событие

запрос на хранение в json
Уметь создавать из json и записывать в него

Иметь покрытие тестами
Комментарии на нетривиальных методах и в целом документация
"""
from __future__ import annotations

import json
from datetime import date
from typing import List, Optional


class Event:
    def __init__(self, name: str, description: str, participants: List[str], start_date: date,
                 repeat: Optional[int] = None) -> object:

        self.name = name
        self.description = description
        self.participants = participants
        self.start_date = start_date
        self.repeat = repeat

        self.organizer = participants[0] if participants else None

    def update_event(self, user_id: str, name: Optional[str] = None, description: Optional[str] = None,
                     participants: Optional[List[str]] = None) -> bool:

        if user_id == self.organizer:
            if name:
                self.name = name
            if description:
                self.description = description
            if participants:
                self.participants = participants
            return True
        return False

    def delete_event(self, user_id: str) -> bool:

        if user_id == self.organizer:
            del self
            return True
        return False

    def leave_event(self, user_id: str) -> bool:
        if user_id in self.participants and user_id != self.organizer:
            self.participants.remove(user_id)
            return True
        return False

    @property
    def to_json(self) -> str | None:

        event_dict = {
            "name": self.name,
            "description": self.description,
            "participants": self.participants,
            "start_date": str(self.start_date),
            "repeat": self.repeat,
            "organizer": self.organizer
        }
        return json.dumps(event_dict)

    @classmethod
    def from_json(cls, json_str: str) -> 'Event':
        event_dict = json.loads(json_str)
        return cls(name=event_dict["name"], description=event_dict["description"],
                   participants=event_dict["participants"], start_date=date.fromisoformat(event_dict["start_date"]),
                   repeat=event_dict["repeat"])
