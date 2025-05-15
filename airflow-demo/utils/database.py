"""Connection for databases."""

from urllib.parse import quote_plus

from sqlalchemy import create_engine
from sqlalchemy.engine.base import Connection


def get_postgresql_conn(
    database: str,
    user: str,
    password: str,
    host: str,
    port: int = 5432,
    connect_args: dict | None = None,
) -> Connection:
    """Get PostgreSQL connection."""
    user = quote_plus(user)
    password = quote_plus(password)

    return create_engine(
        f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}",
    ).connect()