from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class Translation(SQLModel, table=True):  # type: ignore
    id: Optional[int] = Field(default=None, primary_key=True)
    text: str
    destination_language: str
    translated_text: str
    query_datetime: datetime = Field(default_factory=datetime.now)
