from collections.abc import Sequence
from datetime import date

from sqlmodel import Session, SQLModel, col, create_engine, delete, select

from models import Card, Translation
from review import local_today, next_box, next_due

DATABASE_URL = "sqlite:///translations.db"
engine = create_engine(DATABASE_URL)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def store_translation(
    text: str,
    destination: str,
    translated_text: str,
    today: date | None = None,
) -> int:
    """Store a lookup, reset its review card, and return its lookup count."""
    today = today or local_today()
    with Session(engine) as session:
        session.add(
            Translation(
                text=text,
                destination_language=destination,
                translated_text=translated_text,
            )
        )
        card = _find_card(session, text, destination) or Card(
            text=text,
            destination_language=destination,
            translated_text=translated_text,
        )
        card.translated_text = translated_text
        card.box = 1
        card.due = today
        session.add(card)
        session.commit()
        return _lookup_count(session, text, destination)


def retrieve_translations(dest_language: str) -> Sequence[Translation]:
    with Session(engine) as session:
        return session.exec(
            select(Translation)
            .where(Translation.destination_language == dest_language)
            .order_by(col(Translation.query_datetime).desc())
        ).all()


def clear_translations(dest_language: str) -> int:
    with Session(engine) as session:
        session.exec(
            delete(Card).where(col(Card.destination_language) == dest_language)
        )
        result = session.exec(
            delete(Translation).where(
                col(Translation.destination_language) == dest_language
            )
        )
        session.commit()
    return result.rowcount


def due_cards(dest_language: str, today: date) -> Sequence[Card]:
    with Session(engine) as session:
        return session.exec(
            select(Card)
            .where(Card.destination_language == dest_language)
            .where(Card.due <= today)
            .order_by(col(Card.box), col(Card.due))
        ).all()


def record_answer(card_id: int | None, correct: bool, today: date) -> None:
    with Session(engine) as session:
        card = session.get_one(Card, card_id)
        card.box = next_box(card.box, correct)
        card.due = next_due(card.box, today)
        session.add(card)
        session.commit()


def _find_card(session: Session, text: str, destination: str) -> Card | None:
    return session.exec(
        select(Card)
        .where(Card.text == text)
        .where(Card.destination_language == destination)
    ).first()


def _lookup_count(session: Session, text: str, destination: str) -> int:
    return len(
        session.exec(
            select(Translation.id)
            .where(Translation.text == text)
            .where(Translation.destination_language == destination)
        ).all()
    )


if __name__ == "__main__":
    create_db_and_tables()
