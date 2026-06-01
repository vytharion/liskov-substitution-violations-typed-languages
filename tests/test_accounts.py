import pytest

from accounts import (
    Account,
    InsufficientFunds,
    OneTimeToken,
    OverdraftAccount,
    RefreshableToken,
    TokenAlreadyConsumed,
    audit_consumed,
    safe_to_charge,
)


def test_account_balance_invariant_holds_on_construction() -> None:
    account = Account(opening_balance=100)
    assert account.balance == 100


def test_account_rejects_negative_opening_balance() -> None:
    with pytest.raises(ValueError, match="opening_balance must be >= 0"):
        Account(opening_balance=-1)


def test_account_withdraw_keeps_balance_non_negative() -> None:
    account = Account(opening_balance=50)
    account.withdraw(30)
    assert account.balance == 20


def test_account_refuses_overwithdraw_to_preserve_invariant() -> None:
    account = Account(opening_balance=50)
    with pytest.raises(InsufficientFunds):
        account.withdraw(100)
    assert account.balance == 50


def test_safe_to_charge_against_base_matches_balance() -> None:
    account = Account(opening_balance=40)
    assert safe_to_charge(account, 40) is True
    assert safe_to_charge(account, 41) is False


def test_overdraft_account_is_statically_an_account() -> None:
    account = OverdraftAccount(opening_balance=10, overdraft_limit=50)
    assert isinstance(account, Account)


def test_overdraft_account_breaks_balance_invariant_via_subclass_api() -> None:
    account = OverdraftAccount(opening_balance=10, overdraft_limit=50)
    account.withdraw(40)
    assert account.balance == -30


def test_overdraft_account_still_enforces_its_own_floor() -> None:
    account = OverdraftAccount(opening_balance=10, overdraft_limit=50)
    with pytest.raises(InsufficientFunds):
        account.withdraw(100)


def test_safe_to_charge_misleads_caller_when_handed_overdraft_subclass() -> None:
    account: Account = OverdraftAccount(opening_balance=10, overdraft_limit=50)
    assert safe_to_charge(account, 40) is False
    account.withdraw(40)
    assert account.balance == -30


def test_one_time_token_starts_active() -> None:
    token = OneTimeToken()
    assert token.is_active is True


def test_one_time_token_becomes_inactive_after_consume() -> None:
    token = OneTimeToken()
    token.consume()
    assert token.is_active is False


def test_one_time_token_rejects_double_consume() -> None:
    token = OneTimeToken()
    token.consume()
    with pytest.raises(TokenAlreadyConsumed):
        token.consume()


def test_audit_consumed_is_stable_for_base_token() -> None:
    token = OneTimeToken()
    token.consume()
    first = audit_consumed(token)
    second = audit_consumed(token)
    assert first is True
    assert second is True


def test_refreshable_token_is_statically_a_one_time_token() -> None:
    token = RefreshableToken()
    assert isinstance(token, OneTimeToken)


def test_refreshable_token_violates_history_constraint() -> None:
    token = RefreshableToken()
    token.consume()
    snapshot = audit_consumed(token)
    token.refresh()
    later = audit_consumed(token)
    assert snapshot is True
    assert later is False


def test_refreshable_token_can_be_consumed_again_after_refresh() -> None:
    token = RefreshableToken()
    token.consume()
    token.refresh()
    token.consume()
    assert token.is_active is False
