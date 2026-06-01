from __future__ import annotations


class TokenAlreadyConsumed(RuntimeError):
    pass


class OneTimeToken:
    # History constraint: is_active is monotonically non-increasing.
    # Once it flips True -> False via consume(), no method may flip it
    # back. Auditors rely on this to treat a consumed token as terminal.
    def __init__(self) -> None:
        self._active = True

    @property
    def is_active(self) -> bool:
        return self._active

    def consume(self) -> None:
        if not self._active:
            raise TokenAlreadyConsumed("token has already been consumed")
        self._active = False


class RefreshableToken(OneTimeToken):
    # History-constraint violation: the parent guarantees the active flag
    # only ever moves True -> False. refresh() flips it back to True, so
    # any audit log that timestamps the first observed inactive state and
    # assumes the token stays inactive afterwards will silently disagree
    # with reality.
    def refresh(self) -> None:
        self._active = True


def audit_consumed(token: OneTimeToken) -> bool:
    # Encodes the parent history constraint: a token observed inactive
    # once is permanently inactive, so a single check is enough.
    if token.is_active:
        return False
    return not token.is_active
