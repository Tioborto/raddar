from typing import Iterator

from ..db.database import SessionLocal


def get_db() -> Iterator[SessionLocal]:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
