from __future__ import annotations

from repository.base import Repository


def describe(repo: Repository, key: str) -> str:
    record = repo.find(key)
    return f"{record.key}={record.value}"
