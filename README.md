# alembic-migration-snippet

A minimal reference project showing how to wire migrations into a
SQLAlchemy 2.x Python app based on this [post](https://gaultier.github.io/blog/I_sped_up_the_test_suite_by_x2.html) approach, but using Alembic.

## Core Idea

Each test creates a db session, which is at the same time a copy of a source of truth db with all the latest migrations. This way we have a fresh db for each testing. Check `config_test.py`. New db copies will be saved at `/tmp`.

Consider this implementation is based on Sqlite, since we can manage the db as a file. Implementing with PostgreSQL, wont work with this snippet as this engine has a client-server architecture (better to just do transactions and rollbacking on each test).


## Requirements

- Python 3.12
- [uv](https://docs.astral.sh/uv/) (manages the virtualenv + dependencies)

## Setup

    uv sync
    mkdir -p /tmp && touch /tmp/mydb.db 

### Run tests

    uv run pytest app/tests

### Alembic

Under `alembic/versions` we have two migrations as example.

    # Apply all pending migrations (we use this to update the db with new migrations)
    uv run alembic upgrade head

    # Auto-generate a new migration from model changes (generates a pending migration)
    uv run alembic revision --autogenerate -m "describe change"

## Project layout

    app/
      main.py                # placeholder entry point
      db/config.py           # SQLAlchemy engine, SessionLocal, Base
      models/                # SQLAlchemy models (Book, ...)
      schemas/               # Pydantic schemas
      repositories/          # Data-access layer
      services/              # Business logic
      tests/                 # pytest suite
      alembic.ini            # Alembic config
      alembic/
        env.py               # Imports Base + models for autogenerate
        versions/            # Migration scripts
