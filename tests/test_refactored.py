from __future__ import annotations

import typing

import pytest

from refactored import (
    Account,
    ActiveToken,
    ConsumedToken,
    Counter,
    Delivered,
    DeliveryFailure,
    DictMessageStore,
    DraftDocument,
    InMemoryRepository,
    InsufficientFunds,
    ListFeedReader,
    LoopbackTransport,
    Message,
    PublishedDocument,
    Record,
    Rectangle,
    Sent,
    SmsNotifier,
    Square,
    StdoutNotifier,
    TlsTransport,
    TransportFailure,
    audit_consumed,
    cache_or_fallback,
    deliver,
    describe,
    safe_to_charge,
    summarize_twice,
    total_area,
    transmit,
)


# ---------------------------------------------------------------------------
# Shapes — sibling sealed hierarchy, no inherited setters
# ---------------------------------------------------------------------------


def test_rectangle_is_immutable() -> None:
    rect = Rectangle(3, 4)
    with pytest.raises(Exception):
        rect.width = 99  # type: ignore[misc]


def test_rectangle_with_width_returns_new_instance() -> None:
    rect = Rectangle(3, 4)
    resized = rect.with_width(10)
    assert rect.width == 3
    assert resized.width == 10
    assert resized.height == 4
    assert resized.area() == 40


def test_square_is_not_a_subclass_of_rectangle() -> None:
    # The whole point: Square does NOT inherit Rectangle. The naive
    # is-a claim from Step 1 is what made set_width/set_height
    # substitution unsafe; here it is structurally impossible to
    # mistake one for the other.
    assert not issubclass(Square, Rectangle)
    assert not isinstance(Square(5), Rectangle)


def test_square_and_rectangle_both_satisfy_shape_protocol() -> None:
    shapes = [Rectangle(3, 4), Square(5)]
    assert total_area(shapes) == 12 + 25


def test_shape_rejects_non_positive_dimensions() -> None:
    with pytest.raises(ValueError):
        Rectangle(0, 5)
    with pytest.raises(ValueError):
        Square(-1)


# ---------------------------------------------------------------------------
# Counter — sealed with @final
# ---------------------------------------------------------------------------


def test_counter_is_marked_final() -> None:
    # Static checkers (mypy) read __final__ at decoration time and reject
    # subclasses. The runtime flag is the visible artefact we can assert.
    assert getattr(Counter, "__final__", False) is True


def test_counter_rejects_negative_step() -> None:
    counter = Counter()
    with pytest.raises(ValueError):
        counter.increment(-1)


def test_counter_increment_advances_value() -> None:
    counter = Counter(start=2)
    counter.increment(3)
    counter.increment()
    assert counter.value == 6


# ---------------------------------------------------------------------------
# Document — two-state machine, edit() only on the draft type
# ---------------------------------------------------------------------------


def test_draft_edit_returns_new_draft() -> None:
    draft = DraftDocument("hello")
    revised = draft.edit("hello world")
    assert draft.body == "hello"
    assert revised.body == "hello world"


def test_publish_returns_published_document() -> None:
    draft = DraftDocument("hello")
    published = draft.publish()
    assert isinstance(published, PublishedDocument)
    assert published.body == "hello"
    assert published.published is True


def test_published_document_has_no_edit_method() -> None:
    # The history constraint is now structural: PublishedDocument simply
    # does not define edit(). Step 4's RevisableDocument added an
    # override to re-permit the transition; here there is nothing to
    # override because the post-publish type doesn't expose the operation.
    published = DraftDocument("hi").publish()
    assert not hasattr(published, "edit")


# ---------------------------------------------------------------------------
# Repository — Protocol-bound Optional return
# ---------------------------------------------------------------------------


def test_in_memory_repository_returns_optional_on_miss() -> None:
    repo = InMemoryRepository()
    repo.save(Record("a", "alpha"))
    assert repo.find("a") == Record("a", "alpha")
    assert repo.find("missing") is None


def test_describe_falls_back_when_record_missing() -> None:
    repo = InMemoryRepository()
    assert describe(repo, "ghost") == "<missing>"
    repo.save(Record("k", "v"))
    assert describe(repo, "k") == "k=v"


def test_repository_protocol_is_a_protocol() -> None:
    # The contract is the Protocol — implementing classes don't inherit
    # from anything. Optional[Record] is part of the signature, not a
    # documented promise the type checker cannot enforce.
    from refactored.repository import Repository

    assert typing.get_origin(Repository) is None  # the class itself
    assert getattr(Repository, "_is_protocol", False) is True


# ---------------------------------------------------------------------------
# Account — @final with overdraft as a constructor parameter
# ---------------------------------------------------------------------------


def test_account_is_marked_final() -> None:
    assert getattr(Account, "__final__", False) is True


def test_account_without_overdraft_behaves_as_before() -> None:
    account = Account(100.0)
    account.withdraw(40.0)
    assert account.balance == 60.0
    with pytest.raises(InsufficientFunds):
        account.withdraw(99.0)


def test_account_with_overdraft_limit_extends_available() -> None:
    account = Account(50.0, overdraft_limit=25.0)
    assert account.available == 75.0
    account.withdraw(70.0)
    assert account.balance == -20.0
    with pytest.raises(InsufficientFunds):
        account.withdraw(10.0)


def test_safe_to_charge_uses_available_not_balance() -> None:
    account = Account(10.0, overdraft_limit=5.0)
    assert safe_to_charge(account, 15.0) is True
    assert safe_to_charge(account, 15.01) is False


# ---------------------------------------------------------------------------
# Token — two-state sealed machine
# ---------------------------------------------------------------------------


def test_active_token_consume_returns_consumed_token() -> None:
    active = ActiveToken("abc")
    consumed = active.consume()
    assert isinstance(consumed, ConsumedToken)
    assert consumed.identifier == "abc"
    assert audit_consumed(consumed) is True


def test_consumed_token_cannot_be_refreshed() -> None:
    consumed = ActiveToken("xyz").consume()
    assert not hasattr(consumed, "refresh")


def test_audit_consumed_distinguishes_active_and_consumed() -> None:
    assert audit_consumed(ActiveToken("a")) is False
    assert audit_consumed(ActiveToken("a").consume()) is True


# ---------------------------------------------------------------------------
# Notifier — Outcome union replaces raised exceptions
# ---------------------------------------------------------------------------


def test_stdout_notifier_returns_delivered() -> None:
    outcome = StdoutNotifier().notify("hi")
    assert isinstance(outcome, Delivered)
    assert outcome.message == "hi"


def test_stdout_notifier_returns_failure_on_empty() -> None:
    outcome = StdoutNotifier().notify("")
    assert isinstance(outcome, DeliveryFailure)


def test_sms_notifier_reports_failure_via_outcome_not_exception() -> None:
    # Step 5's SmsNotifier raised FlakyNetworkError, a sibling of
    # DeliveryFailed that escaped every except clause. Here the
    # "carrier hiccup" is a DeliveryFailure value, part of the
    # statically-known return type — no exception to broaden.
    notifier = SmsNotifier(fail_on="STORM")
    ok = notifier.notify("clear skies")
    assert isinstance(ok, Delivered)
    bad = notifier.notify("STORM warning")
    assert isinstance(bad, DeliveryFailure)
    assert "STORM" in bad.reason


def test_deliver_helper_branches_on_outcome() -> None:
    assert deliver(StdoutNotifier(), "yo") == "ok"
    assert deliver(SmsNotifier(fail_on="X"), "with X").startswith("failed:")


# ---------------------------------------------------------------------------
# Transport — Outcome union for send()
# ---------------------------------------------------------------------------


def test_loopback_transport_returns_sent() -> None:
    outcome = LoopbackTransport().send(b"abc")
    assert isinstance(outcome, Sent)
    assert outcome.bytes_sent == 3


def test_tls_transport_returns_failure_when_aborting() -> None:
    transport = TlsTransport(abort_on=b"bad")
    outcome = transport.send(b"hello bad payload")
    assert isinstance(outcome, TransportFailure)


def test_transmit_helper_branches_on_outcome() -> None:
    assert transmit(LoopbackTransport(), b"hello") == "sent 5 bytes"
    assert transmit(TlsTransport(abort_on=b"X"), b"X-mark").startswith("failed:")


# ---------------------------------------------------------------------------
# Feed — Protocol pins Sequence return so single-pass iterators don't fit
# ---------------------------------------------------------------------------


def test_list_feed_reader_returns_re_iterable_sequence() -> None:
    reader = ListFeedReader(["a", "b", "c", "d"])
    window = reader.recent(3)
    # Sequence supports repeated iteration AND len().
    assert len(window) == 3
    assert list(window) == ["b", "c", "d"]
    assert list(window) == ["b", "c", "d"]


def test_summarize_twice_returns_matching_counts() -> None:
    reader = ListFeedReader(["one", "two", "three"])
    first, second = summarize_twice(reader, 3)
    assert first == 3
    assert second == 3


def test_summarize_twice_is_stable_across_protocol_implementations() -> None:
    # Any FeedReader-protocol implementation that returns a Sequence
    # passes this test; a single-pass iterator would not satisfy the
    # protocol in the first place.
    reader = ListFeedReader(["x", "y"])
    assert summarize_twice(reader, 5) == (2, 2)


# ---------------------------------------------------------------------------
# Inbox — Protocol pins Optional[Message]; no narrowed override fits
# ---------------------------------------------------------------------------


def test_dict_message_store_returns_optional_on_miss() -> None:
    store = DictMessageStore({"k": Message("hello")})
    assert store.find("k") == Message("hello")
    assert store.find("missing") is None


def test_cache_or_fallback_uses_optional_branch() -> None:
    store = DictMessageStore({"k": Message("hello")})
    assert cache_or_fallback(store, "k", "default") == "hello"
    assert cache_or_fallback(store, "ghost", "default") == "default"
