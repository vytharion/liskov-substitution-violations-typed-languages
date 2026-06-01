from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Union, final


@final
@dataclass(frozen=True)
class DraftDocument:
    # Two-state phase split: DraftDocument owns the edit() transition,
    # PublishedDocument does not even define edit(). Step 4's history
    # violation (RevisableDocument re-permitting edit after publish)
    # cannot be expressed because publish() returns a different type
    # that has no mutating method to override.
    body: str = ""

    def edit(self, body: str) -> "DraftDocument":
        return replace(self, body=body)

    def publish(self) -> "PublishedDocument":
        return PublishedDocument(self.body)


@final
@dataclass(frozen=True)
class PublishedDocument:
    body: str

    @property
    def published(self) -> bool:
        return True


Document = Union[DraftDocument, PublishedDocument]
