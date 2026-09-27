from datetime import date, timedelta

import pytest
from sqlalchemy.pool import StaticPool
from sqlmodel import create_engine

import db

TODAY = date(2026, 9, 27)


@pytest.fixture(autouse=True)
def memory_db(monkeypatch: pytest.MonkeyPatch) -> None:
    engine = create_engine("sqlite://", poolclass=StaticPool)
    monkeypatch.setattr(db, "engine", engine)
    db.create_db_and_tables()


def test_new_lookup_creates_card_due_today() -> None:
    db.store_translation("hola", "en", "hello", today=TODAY)

    [card] = db.due_cards("en", TODAY)
    assert (card.text, card.translated_text, card.box) == (
        "hola",
        "hello",
        1,
    )


def test_cards_are_per_language() -> None:
    db.store_translation("hola", "en", "hello", today=TODAY)

    assert db.due_cards("fr", TODAY) == []


def test_correct_answer_moves_card_up_and_out_of_due() -> None:
    db.store_translation("hola", "en", "hello", today=TODAY)
    [card] = db.due_cards("en", TODAY)

    db.record_answer(card.id, correct=True, today=TODAY)

    assert db.due_cards("en", TODAY) == []
    [card] = db.due_cards("en", TODAY + timedelta(days=2))
    assert card.box == 2


def test_wrong_answer_resets_to_box_one() -> None:
    db.store_translation("hola", "en", "hello", today=TODAY)
    [card] = db.due_cards("en", TODAY)
    db.record_answer(card.id, correct=True, today=TODAY)

    db.record_answer(card.id, correct=False, today=TODAY)

    [card] = db.due_cards("en", TODAY + timedelta(days=1))
    assert card.box == 1


def test_repeat_lookup_resets_card_and_counts() -> None:
    db.store_translation("hola", "en", "hello", today=TODAY)
    [card] = db.due_cards("en", TODAY)
    db.record_answer(card.id, correct=True, today=TODAY)

    count = db.store_translation("hola", "en", "hi", today=TODAY)

    assert count == 2
    [card] = db.due_cards("en", TODAY)
    assert (card.box, card.translated_text) == (1, "hi")


def test_clear_translations_removes_cards() -> None:
    db.store_translation("hola", "en", "hello", today=TODAY)

    db.clear_translations("en")

    assert db.retrieve_translations("en") == []
    assert db.due_cards("en", TODAY) == []
