from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Protocol, runtime_checkable


@dataclass(frozen=True)
class Message:
    body: str


@runtime_checkable
class MessageStore(Protocol):
    # Step 5's StrictMessageStore narrowed Optional[Message] to Message
    # and raised KeyError on miss. The protocol here pins the return to
    # Optional[Message]; the narrowed override would no longer satisfy
    # the protocol — a function returning plain Message cannot stand in
    # for a function whose return type includes None as a legal value.
    def find(self, key: str) -> Optional[Message]: ...


class DictMessageStore:
    def __init__(self, items: dict[str, Message]) -> None:
        self._items = dict(items)

    def find(self, key: str) -> Optional[Message]:
        return self._items.get(key)


def cache_or_fallback(store: MessageStore, key: str, fallback: str) -> str:
    found = store.find(key)
    if found is None:
        return fallback
    return found.body
