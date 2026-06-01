import pytest

from notifications import (
    DeliveryFailed,
    FlakyNetworkError,
    Notifier,
    SmsNotifier,
    deliver,
)


def test_base_notifier_accepts_a_valid_message() -> None:
    Notifier().notify("hello")


def test_base_notifier_raises_delivery_failed_on_empty_message() -> None:
    with pytest.raises(DeliveryFailed):
        Notifier().notify("")


def test_deliver_against_base_returns_ok_on_success() -> None:
    assert deliver(Notifier(), "ping") == "ok"


def test_deliver_against_base_catches_delivery_failed_cleanly() -> None:
    result = deliver(Notifier(), "")
    assert result.startswith("failed: ")


def test_sms_notifier_is_statically_a_notifier() -> None:
    assert isinstance(SmsNotifier(), Notifier)


def test_sms_notifier_passes_through_on_clean_message() -> None:
    SmsNotifier(fail_on="STORM").notify("hello")


def test_sms_notifier_raises_a_broader_exception_class() -> None:
    sms = SmsNotifier(fail_on="STORM")
    with pytest.raises(FlakyNetworkError):
        sms.notify("warning STORM imminent")


def test_flaky_network_error_is_not_a_delivery_failed() -> None:
    assert not issubclass(FlakyNetworkError, DeliveryFailed)


def test_deliver_loses_messages_from_broadened_exception_surface() -> None:
    sms: Notifier = SmsNotifier(fail_on="STORM")
    with pytest.raises(FlakyNetworkError):
        deliver(sms, "warning STORM imminent")


def test_deliver_still_handles_delivery_failed_on_sms_notifier() -> None:
    sms: Notifier = SmsNotifier(fail_on="STORM")
    result = deliver(sms, "")
    assert result.startswith("failed: ")
