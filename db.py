from sqlmodel import Session, SQLModel, create_engine, select

from models import Translation

DATABASE_URL = "sqlite:///translations.db"
engine = create_engine(DATABASE_URL)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def store_translation(text: str, destination: str, translated_text: str):
    with Session(engine) as session:
        translation = Translation(
            text=text, destination_language=destination, translated_text=translated_text
        )
        session.add(translation)
        session.commit()


def retrieve_translations(dest_language: str):
    with Session(engine) as session:
        translations = (
            session.query(Translation)
            .filter_by(destination_language=dest_language)
            .order_by(Translation.query_datetime.desc())
            .all()
        )
        return translations


if __name__ == "__main__":
    create_db_and_tables()
