import pytest

from shapes import BoundedRectangle, Rectangle


def grow_to_target_side(rect: Rectangle, target: float) -> None:
    rect.set_width(target)
    rect.set_height(target)


def test_rectangle_setter_accepts_any_positive_width() -> None:
    rect = Rectangle(2, 3)
    rect.set_width(10_000)
    assert rect.width == 10_000


def test_bounded_rectangle_accepts_in_range_side() -> None:
    bounded = BoundedRectangle(2, 3, max_side=10)
    bounded.set_width(7)
    bounded.set_height(4)
    assert bounded.width == 7
    assert bounded.height == 4
    assert bounded.area() == 28


def test_bounded_rectangle_rejects_width_above_max() -> None:
    bounded = BoundedRectangle(2, 3, max_side=10)
    with pytest.raises(ValueError, match="outside permitted range"):
        bounded.set_width(10_000)


def test_bounded_rectangle_rejects_height_above_max() -> None:
    bounded = BoundedRectangle(2, 3, max_side=10)
    with pytest.raises(ValueError, match="outside permitted range"):
        bounded.set_height(11)


def test_bounded_rectangle_rejects_nonpositive_side() -> None:
    bounded = BoundedRectangle(2, 3, max_side=10)
    with pytest.raises(ValueError):
        bounded.set_width(0)


def test_grow_helper_works_for_plain_rectangle() -> None:
    plain = Rectangle(2, 3)
    grow_to_target_side(plain, 500)
    assert plain.area() == 500 * 500


def test_grow_helper_breaks_when_handed_bounded_subclass() -> None:
    bounded = BoundedRectangle(2, 3, max_side=10)
    with pytest.raises(ValueError):
        grow_to_target_side(bounded, 500)


def test_bounded_rectangle_is_statically_a_rectangle() -> None:
    bounded = BoundedRectangle(2, 3, max_side=10)
    assert isinstance(bounded, Rectangle)
