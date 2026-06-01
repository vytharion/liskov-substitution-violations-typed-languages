from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, Union, runtime_checkable


@dataclass(frozen=True)
class Delivered:
    message: str


@dataclass(frozen=True)
class DeliveryFailure:
    reason: str


# Closed sum: every outcome of notify() is one of these two tags.
Outcome = Union[Delivered, DeliveryFailure]


@runtime_checkable
class Notifier(Protocol):
    # Step 5's SmsNotifier broadened the exception surface past
    # DeliveryFailed by raising a sibling RuntimeException. Returning an
    # Outcome instead of raising removes the broadening lever entirely.
    # Every implementation HAS to produce one of two tagged values; there
    # is no third-class exception escape hatch the type checker would miss.
    def notify(self, message: str) -> Outcome: ...


class StdoutNotifier:
    def notify(self, message: str) -> Outcome:
        if not message:
            return DeliveryFailure("message must be non-empty")
        return Delivered(message)


class SmsNotifier:
    def __init__(self, fail_on: str | None = None) -> None:
        self._fail_on = fail_on

    def notify(self, message: str) -> Outcome:
        if not message:
            return DeliveryFailure("message must be non-empty")
        if self._fail_on is not None and self._fail_on in message:
            return DeliveryFailure(f"carrier hiccup on '{message}'")
        return Delivered(message)


def deliver(notifier: Notifier, message: str) -> str:
    outcome = notifier.notify(message)
    if isinstance(outcome, DeliveryFailure):
        return f"failed: {outcome.reason}"
    return "ok"
