import os
from typing import Generator
from urllib.parse import quote_plus

from dotenv import load_dotenv
from sqlalchemy import Engine
from sqlmodel import create_engine, SQLModel, Session

load_dotenv()

engine: Engine | None = None


def open_postgres_connection() -> None:
    """
    Opens a connection to the PostgreSQL database.
    """
    global engine

    db_user: str = quote_plus(os.getenv("POSTGRES_USERNAME"))
    db_user_password: str = quote_plus(os.getenv("POSTGRES_PASSWORD"))
    db_name: str = os.getenv("POSTGRES_DB_NAME", "smaji")
    connection_uri: str = f"postgresql://{db_user}:{db_user_password}@localhost:5432/{db_name}"

    # Create engine with connection pooling
    engine = create_engine(
        connection_uri,
        echo=True,
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=10
    )

    # Create all tables defined in SQLModel models
    SQLModel.metadata.create_all(engine)

    print("PostgreSQL connection established and tables created successfully.")


def close_postgres_connection() -> None:
    """
    Closes the connection to the PostgreSQL database.
    """
    global engine

    if engine:
        engine.dispose()

    print("PostgreSQL connection closed successfully.")


def get_engine() -> Engine:
    """
    Returns the database engine.
    """

    global engine
    if engine is None:
        raise Exception("Database engine not initialized.")
    return engine


def get_db() -> Generator[Session, None, None]:
    """
    Returns a database session.
    """
    with Session(engine) as session:
        yield session
