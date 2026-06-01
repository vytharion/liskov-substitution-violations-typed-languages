from __future__ import annotations


class DeliveryFailed(RuntimeError):
    pass


class FlakyNetworkError(RuntimeError):
    # Deliberately a sibling of DeliveryFailed, not a subclass. Any
    # `except DeliveryFailed` clause written against the base contract
    # will not catch it.
    pass


class Notifier:
    # Documented exception surface: notify() either returns None or
    # raises DeliveryFailed. Callers may treat any other exception class
    # as a programming bug, not a protocol-level delivery failure.
    def notify(self, message: str) -> None:
        if not message:
            raise DeliveryFailed("message must be non-empty")


class SmsNotifier(Notifier):
    # Exception broadening: the parent contract limits the visible
    # failure surface to DeliveryFailed. This subclass raises
    # FlakyNetworkError on carrier hiccups, slipping a new exception
    # class past every caller that wired `try / except DeliveryFailed`
    # around the call.
    def __init__(self, fail_on: str | None = None) -> None:
        self._fail_on = fail_on

    def notify(self, message: str) -> None:
        super().notify(message)
        if self._fail_on is not None and self._fail_on in message:
            raise FlakyNetworkError(f"carrier hiccup on '{message}'")


def deliver(notifier: Notifier, message: str) -> str:
    # Encodes the documented Notifier contract: the only protocol-level
    # failure mode is DeliveryFailed. Anything broader escapes here and
    # the caller crashes with an exception its except clause never saw.
    try:
        notifier.notify(message)
    except DeliveryFailed as exc:
        return f"failed: {exc}"
    return "ok"
