import pytest

from shapes import PositiveRectangle, Rectangle


def resize_to_zero_width(rect: Rectangle) -> None:
    rect.set_width(0)


def test_rectangle_setter_accepts_zero_width() -> None:
    rect = Rectangle(2, 3)
    rect.set_width(0)
    assert rect.width == 0
    assert rect.area() == 0


def test_rectangle_setter_accepts_negative_width() -> None:
    rect = Rectangle(2, 3)
    rect.set_width(-5)
    assert rect.width == -5


def test_positive_rectangle_accepts_positive_dimensions() -> None:
    rect = PositiveRectangle(4, 5)
    assert rect.width == 4
    assert rect.height == 5
    assert rect.area() == 20


def test_positive_rectangle_rejects_zero_width_in_constructor() -> None:
    with pytest.raises(ValueError, match="width must be positive"):
        PositiveRectangle(0, 3)


def test_positive_rectangle_rejects_negative_height_in_constructor() -> None:
    with pytest.raises(ValueError, match="height must be positive"):
        PositiveRectangle(2, -1)


def test_positive_rectangle_rejects_zero_via_setter() -> None:
    rect = PositiveRectangle(2, 3)
    with pytest.raises(ValueError, match="width must be positive"):
        rect.set_width(0)


def test_positive_rectangle_rejects_negative_via_height_setter() -> None:
    rect = PositiveRectangle(2, 3)
    with pytest.raises(ValueError, match="height must be positive"):
        rect.set_height(-4)


def test_resize_helper_works_on_plain_rectangle() -> None:
    plain = Rectangle(2, 3)
    resize_to_zero_width(plain)
    assert plain.width == 0


def test_resize_helper_breaks_when_handed_positive_subclass() -> None:
    strict = PositiveRectangle(2, 3)
    with pytest.raises(ValueError):
        resize_to_zero_width(strict)


def test_positive_rectangle_is_statically_a_rectangle() -> None:
    rect = PositiveRectangle(2, 3)
    assert isinstance(rect, Rectangle)
