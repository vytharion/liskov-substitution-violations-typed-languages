import pytest

from contracts import Counter, FlexibleCounter


def replay_and_collect_history(counter: Counter, steps: list[int]) -> list[int]:
    history = [counter.value]
    for step in steps:
        counter.increment(step)
        history.append(counter.value)
    return history


def is_monotonic_non_decreasing(values: list[int]) -> bool:
    return all(b >= a for a, b in zip(values, values[1:]))


def test_counter_starts_at_zero_by_default() -> None:
    c = Counter()
    assert c.value == 0


def test_counter_accepts_nonnegative_increment() -> None:
    c = Counter(10)
    c.increment(3)
    c.increment(0)
    c.increment(7)
    assert c.value == 20


def test_counter_rejects_negative_increment() -> None:
    c = Counter()
    with pytest.raises(ValueError, match="requires by >= 0"):
        c.increment(-1)


def test_replay_against_base_counter_produces_monotonic_history() -> None:
    c = Counter(5)
    history = replay_and_collect_history(c, [2, 0, 4, 1])
    assert history == [5, 7, 7, 11, 12]
    assert is_monotonic_non_decreasing(history) is True


def test_flexible_counter_accepts_negative_increment_locally() -> None:
    c = FlexibleCounter(10)
    c.increment(-4)
    assert c.value == 6


def test_replay_against_flexible_counter_breaks_monotonic_invariant() -> None:
    c = FlexibleCounter(5)
    history = replay_and_collect_history(c, [2, -3, 4])
    assert history == [5, 7, 4, 8]
    assert is_monotonic_non_decreasing(history) is False


def test_flexible_counter_is_statically_a_counter() -> None:
    c = FlexibleCounter()
    assert isinstance(c, Counter)
