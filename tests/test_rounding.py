from shapes import Rectangle, RoundingRectangle


def widen_and_verify(rect: Rectangle, width: float) -> bool:
    rect.set_width(width)
    return rect.width == width


def heighten_and_verify(rect: Rectangle, height: float) -> bool:
    rect.set_height(height)
    return rect.height == height


def test_rectangle_setter_preserves_fractional_width() -> None:
    rect = Rectangle(2, 3)
    rect.set_width(2.7)
    assert rect.width == 2.7


def test_rounding_rectangle_rounds_fractional_width_in_setter() -> None:
    snap = RoundingRectangle(2, 3)
    snap.set_width(2.7)
    assert snap.width == 3


def test_rounding_rectangle_rounds_dimensions_in_constructor() -> None:
    snap = RoundingRectangle(2.4, 3.6)
    assert snap.width == 2
    assert snap.height == 4


def test_rounding_rectangle_rounds_height_in_setter() -> None:
    snap = RoundingRectangle(2, 3)
    snap.set_height(4.49)
    assert snap.height == 4


def test_plain_rectangle_satisfies_width_setter_postcondition() -> None:
    rect = Rectangle(2, 3)
    assert widen_and_verify(rect, 3.5) is True
    assert widen_and_verify(rect, 0.1) is True


def test_rounding_rectangle_violates_width_setter_postcondition() -> None:
    snap = RoundingRectangle(2, 3)
    assert widen_and_verify(snap, 3.5) is False


def test_rounding_rectangle_violates_height_setter_postcondition() -> None:
    snap = RoundingRectangle(2, 3)
    assert heighten_and_verify(snap, 7.2) is False


def test_rounding_rectangle_area_uses_rounded_dimensions() -> None:
    snap = RoundingRectangle(2.6, 3.4)
    assert snap.area() == 9


def test_rounding_rectangle_is_statically_a_rectangle() -> None:
    snap = RoundingRectangle(2, 3)
    assert isinstance(snap, Rectangle)
