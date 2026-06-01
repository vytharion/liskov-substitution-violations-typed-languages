from __future__ import annotations


class DocumentLocked(PermissionError):
    pass


class Document:
    # History constraint: once publish() runs, the document is sealed for
    # the rest of its life. The parent honors this by raising on any later
    # edit attempt — callers downstream can cache body without worrying
    # about post-publish drift.
    def __init__(self, body: str = "") -> None:
        self._body = body
        self._published = False

    @property
    def body(self) -> str:
        return self._body

    @property
    def published(self) -> bool:
        return self._published

    def edit(self, body: str) -> None:
        if self._published:
            raise DocumentLocked("published documents are immutable")
        self._body = body

    def publish(self) -> None:
        self._published = True


class RevisableDocument(Document):
    # History-constraint violation: the parent forbids the transition
    # published=True -> body mutated. This override silently re-permits
    # that transition, so any cache or audit trail that trusted the parent
    # contract now observes a body the publisher never approved.
    def edit(self, body: str) -> None:
        self._body = body
