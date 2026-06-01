from __future__ import annotations

from typing import final


class InsufficientFunds(ValueError):
    pass


@final
class Account:
    # Step 4's OverdraftAccount weakened the balance >= 0 invariant by
    # overriding withdraw. Here Account is @final and the "overdraft"
    # concept is moved from a subclass into a constructor parameter on
    # the same class. There is no inheritance lever to pull, so the
    # invariant the callers depend on — balance >= -overdraft_limit —
    # is the same one this class enforces, with no override to weaken it.
    __final__ = True

    def __init__(self, opening_balance: float, overdraft_limit: float = 0.0) -> None:
        if opening_balance < -overdraft_limit:
            raise ValueError(
                f"opening_balance {opening_balance} below overdraft floor "
                f"{-overdraft_limit}"
            )
        if overdraft_limit < 0:
            raise ValueError(f"overdraft_limit must be >= 0, got {overdraft_limit}")
        self._balance = opening_balance
        self._overdraft_limit = overdraft_limit

    @property
    def balance(self) -> float:
        return self._balance

    @property
    def overdraft_limit(self) -> float:
        return self._overdraft_limit

    @property
    def available(self) -> float:
        return self._balance + self._overdraft_limit

    def deposit(self, amount: float) -> None:
        _reject_negative(amount, "deposit")
        self._balance += amount

    def withdraw(self, amount: float) -> None:
        _reject_negative(amount, "withdraw")
        if amount > self.available:
            raise InsufficientFunds(
                f"cannot withdraw {amount}; available is {self.available}"
            )
        self._balance -= amount


def safe_to_charge(account: Account, amount: float) -> bool:
    # The invariant the caller relies on is now in the signature of the
    # only Account class: amount <= available. There is no subclass that
    # can quietly redefine "available".
    return amount <= account.available


def _reject_negative(amount: float, op: str) -> None:
    if amount < 0:
        raise ValueError(f"{op} amount must be >= 0, got {amount}")
