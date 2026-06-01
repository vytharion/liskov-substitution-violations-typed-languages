from __future__ import annotations

from typing import Optional


class Message:
    def __init__(self, body: str) -> None:
        self.body = body


class MessageStore:
    # Documented return contract: find(key) returns either a Message or
    # None. Callers branch on the None case to provide a default,
    # short-circuit a cache miss, or log absence without raising.
    def __init__(self, items: dict[str, Message]) -> None:
        self._items = dict(items)

    def find(self, key: str) -> Optional[Message]:
        return self._items.get(key)


class StrictMessageStore(MessageStore):
    # Covariant return abuse: Message is a structural subtype of
    # Optional[Message], so the type checker accepts the narrowed
    # return signature (this mirrors Java/C# covariant return overrides
    # and TypeScript structural subtyping). But callers that branch on
    # None against the base contract observe a thrown KeyError instead
    # — the None branch becomes dead code, and the crash surfaces in
    # production the first time a cache miss happens.
    def find(self, key: str) -> Message:  # type: ignore[override]
        item = self._items.get(key)
        if item is None:
            raise KeyError(f"no message for {key}")
        return item


def cache_or_fallback(store: MessageStore, key: str, fallback: str) -> str:
    # Encodes the documented Optional return contract: on a miss the
    # caller returns the fallback. Against the base this works. Against
    # StrictMessageStore the miss path raises KeyError before this
    # branch can execute — the static signature LIED about the runtime
    # behavior, and every caller that trusted the base contract crashes.
    found = store.find(key)
    if found is None:
        return fallback
    return found.body
