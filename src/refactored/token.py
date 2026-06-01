from __future__ import annotations

from dataclasses import dataclass
from typing import final


@final
@dataclass(frozen=True)
class ActiveToken:
    # Two-state sealed model: an ActiveToken can only become a
    # ConsumedToken, and ConsumedToken has no refresh() method to override.
    # Step 4's RefreshableToken flipped the monotonic flag back by adding
    # a method on the same class; under this split there is no class
    # whose API exposes both "consumed" and "refresh", so the
    # history constraint is enforced by which type a caller holds.
    identifier: str

    def consume(self) -> "ConsumedToken":
        return ConsumedToken(self.identifier)


@final
@dataclass(frozen=True)
class ConsumedToken:
    identifier: str

    @property
    def is_active(self) -> bool:
        return False


Token = ActiveToken | ConsumedToken


def audit_consumed(token: Token) -> bool:
    return isinstance(token, ConsumedToken)
