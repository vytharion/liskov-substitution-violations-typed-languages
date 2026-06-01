from __future__ import annotations


class TransportError(RuntimeError):
    pass


class TransportClosed(TransportError):
    # Subclass of TransportError. A caller's `except TransportError`
    # clause catches this case, so the documented surface holds.
    pass


class HandshakeAborted(RuntimeError):
    # Sibling, NOT a subclass of TransportError. Any caller that wires
    # `except TransportError` around send() will miss it entirely — the
    # exact pattern Java's `throws` declaration is supposed to prevent
    # but that a subclass can still smuggle past by widening with a
    # runtime exception class outside the declared hierarchy.
    pass


class Transport:
    # Documented exception surface: send() either returns the number of
    # bytes accepted or raises TransportError (or one of its subclasses).
    # Anything broader is a protocol-level break, not a delivery failure.
    def send(self, payload: bytes) -> int:
        if not payload:
            raise TransportError("payload is empty")
        return len(payload)


class TlsTransport(Transport):
    # Exception broadening: the override widens the visible failure
    # surface to include HandshakeAborted, a sibling class no base
    # contract catch clause can trap. Static typing accepts this because
    # Python (like C# and TypeScript) does not enforce checked exception
    # signatures — and even Java cannot stop a subclass from throwing
    # an unchecked RuntimeException it never declared.
    def __init__(self, abort_on: bytes | None = None) -> None:
        self._abort_on = abort_on

    def send(self, payload: bytes) -> int:
        if self._abort_on is not None and self._abort_on in payload:
            raise HandshakeAborted("tls handshake aborted")
        return super().send(payload)


def transmit(transport: Transport, payload: bytes) -> str:
    # Encodes the documented Transport contract: TransportError is the
    # only protocol-level failure mode. Anything broader escapes here
    # and the caller crashes with an exception its except clause never
    # saw — the bug surfaces as an unhandled stack trace in production.
    try:
        sent = transport.send(payload)
    except TransportError as exc:
        return f"failed: {exc}"
    return f"sent {sent} bytes"
