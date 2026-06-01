from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, Union, runtime_checkable


@dataclass(frozen=True)
class Sent:
    bytes_sent: int


@dataclass(frozen=True)
class TransportFailure:
    reason: str


SendOutcome = Union[Sent, TransportFailure]


@runtime_checkable
class Transport(Protocol):
    # Same shape as Notifier: an Outcome union closes off the exception
    # broadening Step 5 exhibited with HandshakeAborted (a sibling, not a
    # subclass, of TransportError). There is no "anything broader" to
    # smuggle through — every failure tag is part of the return type.
    def send(self, payload: bytes) -> SendOutcome: ...


class LoopbackTransport:
    def send(self, payload: bytes) -> SendOutcome:
        if not payload:
            return TransportFailure("payload is empty")
        return Sent(len(payload))


class TlsTransport:
    def __init__(self, abort_on: bytes | None = None) -> None:
        self._abort_on = abort_on

    def send(self, payload: bytes) -> SendOutcome:
        if not payload:
            return TransportFailure("payload is empty")
        if self._abort_on is not None and self._abort_on in payload:
            return TransportFailure("tls handshake aborted")
        return Sent(len(payload))


def transmit(transport: Transport, payload: bytes) -> str:
    outcome = transport.send(payload)
    if isinstance(outcome, TransportFailure):
        return f"failed: {outcome.reason}"
    return f"sent {outcome.bytes_sent} bytes"
