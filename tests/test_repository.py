import pytest

from repository import (
    LenientRepository,
    Record,
    RecordNotFound,
    Repository,
    describe,
)


def test_repository_find_returns_stored_record() -> None:
    repo = Repository()
    repo.save(Record("alpha", "1"))
    assert repo.find("alpha") == Record("alpha", "1")


def test_repository_find_raises_on_miss() -> None:
    repo = Repository()
    with pytest.raises(RecordNotFound):
        repo.find("missing")


def test_describe_against_base_returns_formatted_record() -> None:
    repo = Repository()
    repo.save(Record("alpha", "1"))
    assert describe(repo, "alpha") == "alpha=1"


def test_describe_against_base_propagates_record_not_found() -> None:
    repo = Repository()
    with pytest.raises(RecordNotFound):
        describe(repo, "missing")


def test_lenient_repository_returns_none_on_miss() -> None:
    repo = LenientRepository()
    assert repo.find("missing") is None


def test_lenient_repository_still_returns_stored_record() -> None:
    repo = LenientRepository()
    repo.save(Record("alpha", "1"))
    assert repo.find("alpha") == Record("alpha", "1")


def test_describe_crashes_against_lenient_repository_on_miss() -> None:
    repo = LenientRepository()
    with pytest.raises(AttributeError):
        describe(repo, "missing")


def test_lenient_repository_is_statically_a_repository() -> None:
    repo = LenientRepository()
    assert isinstance(repo, Repository)
