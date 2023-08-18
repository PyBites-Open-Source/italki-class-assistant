from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field


class Translation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    text: str
    destination_language: str
    translated_text: str
    query_datetime: datetime = Field(default_factory=datetime.now)
