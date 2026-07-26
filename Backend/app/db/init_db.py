from sqlalchemy import text

from app.db.session import engine


def init_database() -> None:

    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    print("Database Connected Successfully")


if __name__ == "__main__":
    init_database()