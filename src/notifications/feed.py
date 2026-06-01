from __future__ import annotations

from typing import Iterable, Iterator


class FeedReader:
    # Documented return contract: recent(n) returns a re-iterable
    # sequence. Callers may walk it more than once and observe the same
    # items each pass — caches and audit replays rely on this.
    def __init__(self, items: list[str]) -> None:
        self._items = list(items)

    def recent(self, n: int) -> Iterable[str]:
        return list(self._items[-n:])


class StreamingFeedReader(FeedReader):
    # Covariant return abuse: Iterator[str] is a structural subtype of
    # Iterable[str], so the type checker accepts the override. But an
    # iterator is single-pass — callers that walk the return value
    # twice silently observe an empty sequence on the second walk.
    def recent(self, n: int) -> Iterator[str]:
        for item in self._items[-n:]:
            yield item


def summarize_twice(reader: FeedReader, n: int) -> tuple[int, int]:
    # Encodes the documented re-iterable contract: the caller asks for a
    # window once, then walks the result twice. Against the base both
    # counts must match.
    items = reader.recent(n)
    first = sum(1 for _ in items)
    second = sum(1 for _ in items)
    return first, second
