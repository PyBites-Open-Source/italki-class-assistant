from datetime import date, datetime
from typing import Optional

from pydantic import NaiveDatetime
from sqlmodel import Field, SQLModel


class Translation(SQLModel, table=True):  # type: ignore
    id: Optional[int] = Field(default=None, primary_key=True)
    text: str
    destination_language: str
    translated_text: str
    query_datetime: NaiveDatetime = Field(default_factory=datetime.now)


class Card(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    text: str
    destination_language: str
    translated_text: str
    box: int = 1
    due: date = Field(default_factory=date.today)
