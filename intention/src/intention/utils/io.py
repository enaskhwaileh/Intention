import json
from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Iterable

from pydantic import BaseModel


def read_jsonl(path: str | Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def write_jsonl(path: str | Path, rows: Iterable[object]) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(_to_jsonable(row)) + "\n")


def _to_jsonable(row: object) -> object:
    if isinstance(row, BaseModel):
        return row.model_dump()
    if is_dataclass(row):
        return asdict(row)
    return row
