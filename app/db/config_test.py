import contextlib
import hashlib
import os
import shutil
import sqlite3
from pathlib import Path
from typing import List
from alembic.config import Config, command
from alembic.script import Script, ScriptDirectory
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from utils import get_root_path


@contextlib.contextmanager
def open_test_session():
    golden_db = GoldenDb(auto_rm=True)
    database_path = golden_db.acquire_test_database_path()

    engine = create_engine(f"sqlite:///{database_path}")
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    try:
        yield db
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()
        engine.dispose() # important for testing; cleans the connection pool

        try:
            if golden_db.auto_rm:
                database_path.unlink()
        except OSError:
            pass


class GoldenDb:
    TMP_DIR = Path("/tmp")

    def __init__(self, auto_rm: bool = False) -> None:
        self.alembic_config = Config(str(get_root_path() / "alembic.ini"))
        self.alembic_script_dir = ScriptDirectory.from_config(self.alembic_config)
        self.migration_revisions = self._collect_migrations()
        self.migrations_hash = self._compute_migrations_hash()
        self.auto_rm = auto_rm

    def create_golden_database(self) -> Path:
        print("Creating new golden database...")
        random_name = hashlib.sha256(os.urandom(16)).hexdigest()
        temp_path = self.TMP_DIR / f"{random_name}.db"

        self.alembic_config.set_main_option("sqlalchemy.url", f"sqlite:///{temp_path}")

        print("Setting up migrations...")
        try:
            command.upgrade(self.alembic_config, "head")
        except Exception:
            temp_path.unlink(missing_ok=True)
            raise

        with sqlite3.connect(temp_path) as test_db:
            test_db.execute("SELECT 1")

        print("Renaming database...")
        golden_path = temp_path.rename(self.TMP_DIR / f"{self.migrations_hash}.db")

        print("Golden database created!!")
        with sqlite3.connect(golden_path) as golden_db_conn:
            golden_db_conn.execute("DELETE FROM book")
            golden_db_conn.commit()

        return golden_path

    def acquire_test_database_path(self) -> Path:
        golden_path = self.TMP_DIR / f"{self.migrations_hash}.db"

        if not golden_path.exists():
            self.create_golden_database()

        clone_path = self._copy_db(golden_path)
        self.alembic_config.set_main_option("sqlalchemy.url", f"sqlite:///{clone_path}")

        return clone_path

    def _collect_migrations(self) -> List[Script]:
        revisions = list(self.alembic_script_dir.walk_revisions(base="base", head="heads"))
        revisions = list(reversed(revisions))

        return revisions

    def _compute_migrations_hash(self) -> str:
        revision_ids = "::".join(r.revision for r in self.migration_revisions)
        return hashlib.sha256(revision_ids.encode(encoding="utf-8")).hexdigest()

    def _copy_db(self, golden_path: Path) -> Path:
        print("Cloning db for testing...")
        random_name = hashlib.sha256(os.urandom(16)).hexdigest() + ".db"
        clone_path = golden_path.with_name(random_name)
        shutil.copyfile(golden_path, clone_path)
        print(f"DB {random_name} copied")

        return clone_path
