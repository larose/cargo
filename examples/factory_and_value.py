import abc
import typing

import cargo

DatabaseURL = typing.NewType("DatabaseURL", str)


class DatabaseClient(abc.ABC):
    pass


class MysqlClient(DatabaseClient):
    def __init__(self, db_url: DatabaseURL):
        pass


class PostgresClient(DatabaseClient):
    def __init__(self, db_url: DatabaseURL):
        pass


def database_client_factory(db_url: DatabaseURL) -> DatabaseClient:
    if db_url.startswith("mysql://"):
        return MysqlClient(db_url)

    if db_url.startswith("postgres://"):
        return PostgresClient(db_url)

    raise Exception(f"Invalid database url: {db_url}")


container = cargo.containers.Standard()

# Registers a factory
container[DatabaseClient] = database_client_factory

# Registers a value
container[DatabaseURL] = "mysql://user:password@host:3306/db"

db_client = container[DatabaseClient]

print(db_client)  # Prints: <__main__.MysqlClient object at 0x7f681975b390>
