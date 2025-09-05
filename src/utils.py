import json
from pathlib import Path
from typing import Any


def writeJSON(path: str, obj: Any, complete: bool = False):
    if complete:
        filename = Path(path)
    else:
        dirname = Path(__file__).parent / "database"
        dirname.mkdir(exist_ok=True)
        filename = dirname / path

    if not filename.exists():
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(obj, f, ensure_ascii=False, indent=2)


def readJSON(path: str, complete: bool = False):
    if complete:
        filename = Path(path)
    else:
        dirname = Path(__file__).parent / "database"
        filename = dirname / path

    if filename.exists():
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


def file_exists(path: str, complete: bool = False) -> bool:
    if complete:
        filename = Path(path)
    else:
        dirname = Path(__file__).parent / "database"
        filename = dirname / path
    return filename.exists()
