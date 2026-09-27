from datetime import date, datetime, timedelta

MAX_BOX = 5


def next_box(box: int, correct: bool) -> int:
    return min(box + 1, MAX_BOX) if correct else 1


def next_due(box: int, today: date) -> date:
    return today + timedelta(days=2 ** (box - 1))


def local_today() -> date:
    return datetime.now().astimezone().date()
