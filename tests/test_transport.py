import pytest

from transports import (
    HandshakeAborted,
    TlsTransport,
    Transport,
    TransportClosed,
    TransportError,
    transmit,
)


def test_base_transport_accepts_a_non_empty_payload() -> None:
    assert Transport().send(b"hello") == 5


def test_base_transport_raises_transport_error_on_empty_payload() -> None:
    with pytest.raises(TransportError):
        Transport().send(b"")


def test_transport_closed_is_caught_by_transport_error_clause() -> None:
    assert issubclass(TransportClosed, TransportError)


def test_handshake_aborted_is_not_a_transport_error() -> None:
    assert not issubclass(HandshakeAborted, TransportError)


def test_transmit_against_base_reports_byte_count_on_success() -> None:
    assert transmit(Transport(), b"ping") == "sent 4 bytes"


def test_transmit_against_base_catches_transport_error_cleanly() -> None:
    result = transmit(Transport(), b"")
    assert result.startswith("failed: ")


def test_tls_transport_is_statically_a_transport() -> None:
    assert isinstance(TlsTransport(), Transport)


def test_tls_transport_passes_through_on_clean_payload() -> None:
    assert TlsTransport(abort_on=b"BAD").send(b"hello") == 5


def test_tls_transport_raises_a_sibling_exception_class() -> None:
    tls = TlsTransport(abort_on=b"BAD")
    with pytest.raises(HandshakeAborted):
        tls.send(b"BAD payload")


def test_transmit_loses_messages_from_broadened_exception_surface() -> None:
    tls: Transport = TlsTransport(abort_on=b"BAD")
    with pytest.raises(HandshakeAborted):
        transmit(tls, b"BAD payload")


def test_transmit_still_catches_transport_error_on_tls_transport() -> None:
    tls: Transport = TlsTransport(abort_on=b"BAD")
    result = transmit(tls, b"")
    assert result.startswith("failed: ")
