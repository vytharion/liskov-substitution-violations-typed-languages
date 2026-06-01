from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Protocol, runtime_checkable


@dataclass(frozen=True)
class Record:
    key: str
    value: str


@runtime_checkable
class Repository(Protocol):
    # Trait-style bound: the contract IS the Protocol. find() returns
    # Optional[Record] — the None branch is part of the signature, not a
    # documented promise the type checker cannot see. Step 3's
    # LenientRepository disguised None-on-miss inside a Record return; with
    # the protocol exposing Optional directly, the same implementation is
    # the only thing the type checker will accept, and downstream callers
    # branch on None as a matter of typed routine.
    def save(self, record: Record) -> None: ...
    def find(self, key: str) -> Optional[Record]: ...


class InMemoryRepository:
    def __init__(self) -> None:
        self._store: dict[str, Record] = {}

    def save(self, record: Record) -> None:
        self._store[record.key] = record

    def find(self, key: str) -> Optional[Record]:
        return self._store.get(key)


def describe(repo: Repository, key: str, fallback: str = "<missing>") -> str:
    record = repo.find(key)
    if record is None:
        return fallback
    return f"{record.key}={record.value}"
