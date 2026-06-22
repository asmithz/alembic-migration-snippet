from functools import lru_cache
from pathlib import Path


@lru_cache()
def get_root_path() -> Path:
    """ Returns absoulte path until /app"""
    root_path = Path(__file__).resolve().parent
    return root_path
