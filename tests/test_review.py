from datetime import date

import pytest

from review import MAX_BOX, next_box, next_due

TODAY = date(2026, 9, 27)


@pytest.mark.parametrize(
    ("box", "correct", "expected"),
    [
        (1, True, 2),
        (4, True, 5),
        (MAX_BOX, True, MAX_BOX),
        (1, False, 1),
        (4, False, 1),
    ],
)
def test_next_box(box: int, correct: bool, expected: int) -> None:
    assert next_box(box, correct) == expected


@pytest.mark.parametrize(
    ("box", "expected"),
    [
        (1, date(2026, 9, 28)),
        (2, date(2026, 9, 29)),
        (3, date(2026, 10, 1)),
        (5, date(2026, 10, 13)),
    ],
)
def test_next_due_doubles_interval_per_box(box: int, expected: date) -> None:
    assert next_due(box, TODAY) == expected
