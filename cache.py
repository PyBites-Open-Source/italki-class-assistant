from functools import wraps
from typing import Callable

from sqlalchemy import desc
from sqlmodel import SQLModel, Field, Session, create_engine, select

# SQLite database file
DATABASE_URL = "sqlite:///translation_cache.db"

# SQLModel engine
engine = create_engine(DATABASE_URL)

# Define the TranslationCache model
class TranslationCache(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    source_text: str
    target_language: str
    translated_text: str


# Create the table in the database, if it does not exist
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


# The cache decorator
def cache_translation(func: Callable):
    @wraps(func)
    def wrapper(text: str, target: str = "en"):
        # Create a session
        with Session(engine) as session:
            # Check if this translation is already cached
            statement = select(TranslationCache).where(
                (TranslationCache.source_text == text)
                & (TranslationCache.target_language == target)
            )
            cached_translation = session.exec(statement).first()

            # If cached, return the cached translation
            if cached_translation:
                return cached_translation.translated_text

            # If not, call the original translate function
            translated_text = func(text, target)

            # Cache this new translation in the database
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
    # Create a session
    with Session(engine) as session:
        # Query for translations in the selected target language
        statement = select(TranslationCache).where(
            TranslationCache.target_language == target_language
        ).order_by(desc(TranslationCache.id))
        results = session.exec(statement).all()

    return results


# Call this function when this module is imported
create_db_and_tables()
