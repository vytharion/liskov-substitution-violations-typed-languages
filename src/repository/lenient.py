from __future__ import annotations

from typing import cast

from repository.base import Record, Repository


class LenientRepository(Repository):
    # Postcondition weakening: the base contract guarantees either a Record
    # or RecordNotFound. This override silently returns None on a miss and
    # squeezes it past the static return type via cast, so any caller that
    # trusts the parent guarantee crashes on the first attribute read.
    def find(self, key: str) -> Record:
        return cast(Record, self._store.get(key))
