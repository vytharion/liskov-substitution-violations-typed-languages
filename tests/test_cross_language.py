from __future__ import annotations

from pathlib import Path

import pytest

CROSS_LANGUAGE_ROOT = Path(__file__).resolve().parent.parent / "cross_language"


def _read(relative: str) -> str:
    path = CROSS_LANGUAGE_ROOT / relative
    return path.read_text(encoding="utf-8")


def test_cross_language_root_exists() -> None:
    assert CROSS_LANGUAGE_ROOT.is_dir()


def test_three_language_subdirectories_are_present() -> None:
    for sub in ("java", "csharp", "typescript"):
        assert (CROSS_LANGUAGE_ROOT / sub).is_dir(), sub


def test_java_feed_uses_iterable_to_iterator_narrowing() -> None:
    body = _read("java/Feed.java")
    assert "Iterable<String> recent" in body
    assert "Iterator<String> recent" in body
    assert "@Override" in body


def test_java_notifier_keeps_checked_throws_clause_on_override() -> None:
    body = _read("java/Notifier.java")
    assert "throws DeliveryFailed" in body
    assert "extends BaseNotifier" in body
    assert "FlakyNetworkError" in body
    assert body.count("throws DeliveryFailed") >= 2


def test_csharp_feed_uses_virtual_and_override_with_yield_return() -> None:
    body = _read("csharp/Feed.cs")
    assert "public virtual IEnumerable<string> Recent" in body
    assert "public override IEnumerable<string> Recent" in body
    assert "yield return" in body


def test_csharp_notifier_broadens_the_exception_surface() -> None:
    body = _read("csharp/Notifier.cs")
    assert "class DeliveryFailed : Exception" in body
    assert "class FlakyNetworkError : Exception" in body
    assert "public override void Notify" in body
    assert "throw new FlakyNetworkError" in body


def test_typescript_feed_narrows_iterable_to_generator() -> None:
    body = _read("typescript/feed.ts")
    assert "recent(n: number): Iterable<string>" in body
    assert "recent(n: number): IterableIterator<string>" in body
    assert "*recent" in body


def test_typescript_notifier_broadens_the_exception_surface() -> None:
    body = _read("typescript/notifier.ts")
    assert "class DeliveryFailed extends Error" in body
    assert "class FlakyNetworkError extends Error" in body
    assert "class SmsNotifier extends Notifier" in body
    assert "throw new FlakyNetworkError" in body
    assert "instanceof DeliveryFailed" in body


@pytest.mark.parametrize(
    "relative,sibling_class,base_class",
    [
        ("java/Notifier.java", "FlakyNetworkError", "DeliveryFailed"),
        ("csharp/Notifier.cs", "FlakyNetworkError", "DeliveryFailed"),
        ("typescript/notifier.ts", "FlakyNetworkError", "DeliveryFailed"),
    ],
)
def test_flaky_network_error_is_sibling_not_subclass(
    relative: str, sibling_class: str, base_class: str
) -> None:
    body = _read(relative)
    forbidden = f"{sibling_class} extends {base_class}"
    forbidden_cs = f"{sibling_class} : {base_class}"
    assert forbidden not in body, relative
    assert forbidden_cs not in body, relative
    assert sibling_class in body
    assert base_class in body


@pytest.mark.parametrize(
    "relative,marker",
    [
        ("java/Feed.java", "summarizeTwice"),
        ("csharp/Feed.cs", "SummarizeTwice"),
        ("typescript/feed.ts", "summarizeTwice"),
    ],
)
def test_each_feed_module_ships_a_two_pass_driver(relative: str, marker: str) -> None:
    body = _read(relative)
    assert marker in body, relative
