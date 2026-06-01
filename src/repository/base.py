from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Record:
    key: str
    value: str


class RecordNotFound(LookupError):
    pass


class Repository:
    # Base contract: find(key) returns a fully-populated Record or raises
    # RecordNotFound. Callers may safely read fields on the result without
    # a None check.
    def __init__(self) -> None:
        self._store: dict[str, Record] = {}

    def save(self, record: Record) -> None:
        self._store[record.key] = record

    def find(self, key: str) -> Record:
        if key not in self._store:
            raise RecordNotFound(key)
        return self._store[key]
