from __future__ import annotations


class InsufficientFunds(ValueError):
    pass


class Account:
    # Class invariant: balance >= 0 at every observable moment after
    # construction. Callers may rely on this invariant when sizing a
    # charge against the current balance without an extra range check.
    def __init__(self, opening_balance: float) -> None:
        if opening_balance < 0:
            raise ValueError(f"opening_balance must be >= 0, got {opening_balance}")
        self._balance = opening_balance

    @property
    def balance(self) -> float:
        return self._balance

    def deposit(self, amount: float) -> None:
        self._require_non_negative(amount, "deposit")
        self._balance += amount

    def withdraw(self, amount: float) -> None:
        self._require_non_negative(amount, "withdraw")
        if amount > self._balance:
            raise InsufficientFunds(
                f"cannot withdraw {amount} from balance {self._balance}"
            )
        self._balance -= amount

    @staticmethod
    def _require_non_negative(amount: float, op: str) -> None:
        if amount < 0:
            raise ValueError(f"{op} amount must be >= 0, got {amount}")


class OverdraftAccount(Account):
    # Invariant violation: the parent guarantees balance >= 0. This subclass
    # permits balance to fall to -overdraft_limit. Any caller that trusts
    # the parent invariant (e.g. "balance is the largest safe charge")
    # quietly overcharges and never sees an exception.
    def __init__(self, opening_balance: float, overdraft_limit: float) -> None:
        super().__init__(opening_balance)
        if overdraft_limit < 0:
            raise ValueError(f"overdraft_limit must be >= 0, got {overdraft_limit}")
        self._overdraft_limit = overdraft_limit

    @property
    def overdraft_limit(self) -> float:
        return self._overdraft_limit

    def withdraw(self, amount: float) -> None:
        self._require_non_negative(amount, "withdraw")
        floor = -self._overdraft_limit
        new_balance = self._balance - amount
        if new_balance < floor:
            raise InsufficientFunds(
                f"cannot withdraw {amount}; would breach overdraft floor {floor}"
            )
        self._balance = new_balance


def safe_to_charge(account: Account, amount: float) -> bool:
    # Decision rests on the documented Account invariant: balance >= 0,
    # so balance itself is the maximum charge that cannot overdraw.
    return amount <= account.balance
