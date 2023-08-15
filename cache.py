from functools import wraps
from typing import Callable

from sqlalchemy import desc
from sqlmodel import SQLModel, Field, Session, create_engine, select

DATABASE_URL = "sqlite:///translation_cache.db"

engine = create_engine(DATABASE_URL)


class TranslationCache(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    source_text: str
    target_language: str
    translated_text: str


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def cache_translation(func: Callable):
    @wraps(func)
    def wrapper(text: str, target: str = "en"):
        with Session(engine) as session:
            statement = select(TranslationCache).where(
                (TranslationCache.source_text == text)
                & (TranslationCache.target_language == target)
            )

            cached_translation = session.exec(statement).first()
            if cached_translation:
                return cached_translation.translated_text

            translated_text = func(text, target)
            new_translation = TranslationCache(
                source_text=text,
                target_language=target,
                translated_text=translated_text,
            )
            session.add(new_translation)
            session.commit()
            return translated_text

    return wrapper


def get_translations_for_language(target_language: str):
    with Session(engine) as session:
        statement = select(TranslationCache).where(
            TranslationCache.target_language == target_language
        ).order_by(desc(TranslationCache.id))
        results = session.exec(statement).all()

    return results


create_db_and_tables()
