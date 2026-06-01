from __future__ import annotations

from typing import final


@final
class Counter:
    # The @final decorator instructs static checkers to reject any subclass.
    # Step 4's FlexibleCounter weakened the never-decreases invariant by
    # overriding increment; with Counter sealed at the type level the
    # weakening attempt is a type error before runtime even starts. The
    # invariant — value monotonically non-decreasing — is now structurally
    # guaranteed because no override can change the only mutator.
    def __init__(self, start: int = 0) -> None:
        if start < 0:
            raise ValueError(f"start must be >= 0, got {start}")
        self._value = start

    @property
    def value(self) -> int:
        return self._value

    def increment(self, by: int = 1) -> None:
        if by < 0:
            raise ValueError(f"Counter.increment requires by >= 0, got {by}")
        self._value += by
