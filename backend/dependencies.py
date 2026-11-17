from backend.database import get_db


def get_database():
    yield from get_db()