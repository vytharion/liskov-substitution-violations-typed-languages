from __future__ import annotations

from typing import Protocol, Sequence, runtime_checkable


@runtime_checkable
class FeedReader(Protocol):
    # Step 5's StreamingFeedReader narrowed the return type from
    # Iterable[str] to Iterator[str], satisfying the type checker but
    # silently breaking the re-iterable contract. The protocol here pins
    # the return type to Sequence[str], which DOES NOT admit single-pass
    # iterators — a Sequence supports len(), random access, and repeated
    # iteration, none of which a generator implements. The narrowing
    # attempt now fails the structural subtype check, so the type
    # checker rejects it instead of waving it through.
    def recent(self, n: int) -> Sequence[str]: ...


class ListFeedReader:
    def __init__(self, items: list[str]) -> None:
        self._items = list(items)

    def recent(self, n: int) -> Sequence[str]:
        return tuple(self._items[-n:])


def summarize_twice(reader: FeedReader, n: int) -> tuple[int, int]:
    items = reader.recent(n)
    first = sum(1 for _ in items)
    second = sum(1 for _ in items)
    return first, second
