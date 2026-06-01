import pytest

from transports import (
    Message,
    MessageStore,
    StrictMessageStore,
    cache_or_fallback,
)


def _store(items: dict[str, str]) -> MessageStore:
    return MessageStore({key: Message(body) for key, body in items.items()})


def _strict(items: dict[str, str]) -> StrictMessageStore:
    return StrictMessageStore({key: Message(body) for key, body in items.items()})


def test_base_store_returns_a_message_when_the_key_is_present() -> None:
    store = _store({"a": "alpha"})
    found = store.find("a")
    assert found is not None
    assert found.body == "alpha"


def test_base_store_returns_none_on_a_miss() -> None:
    store = _store({"a": "alpha"})
    assert store.find("b") is None


def test_cache_or_fallback_against_base_returns_message_body_on_hit() -> None:
    store = _store({"a": "alpha"})
    assert cache_or_fallback(store, "a", "missing") == "alpha"


def test_cache_or_fallback_against_base_returns_fallback_on_miss() -> None:
    store = _store({"a": "alpha"})
    assert cache_or_fallback(store, "b", "missing") == "missing"


def test_strict_store_is_statically_a_message_store() -> None:
    assert isinstance(_strict({"a": "alpha"}), MessageStore)


def test_strict_store_returns_a_message_on_hit() -> None:
    store = _strict({"a": "alpha"})
    found = store.find("a")
    assert found.body == "alpha"


def test_strict_store_raises_key_error_on_a_miss() -> None:
    store = _strict({"a": "alpha"})
    with pytest.raises(KeyError):
        store.find("b")


def test_cache_or_fallback_against_strict_store_crashes_on_miss() -> None:
    store: MessageStore = _strict({"a": "alpha"})
    with pytest.raises(KeyError):
        cache_or_fallback(store, "b", "missing")


def test_cache_or_fallback_against_strict_store_still_works_on_hit() -> None:
    store: MessageStore = _strict({"a": "alpha"})
    assert cache_or_fallback(store, "a", "missing") == "alpha"
