from shapes import Rectangle, Shape, Square


def test_rectangle_area_is_width_times_height() -> None:
    rect = Rectangle(3, 4)
    assert rect.area() == 12


def test_rectangle_independent_setters() -> None:
    rect = Rectangle(3, 4)
    rect.set_width(5)
    rect.set_height(6)
    assert rect.width == 5
    assert rect.height == 6
    assert rect.area() == 30


def test_square_initial_area() -> None:
    square = Square(5)
    assert square.area() == 25


def test_square_keeps_invariant_when_width_changes() -> None:
    square = Square(2)
    square.set_width(7)
    assert square.width == 7
    assert square.height == 7
    assert square.area() == 49


def test_square_keeps_invariant_when_height_changes() -> None:
    square = Square(2)
    square.set_height(9)
    assert square.width == 9
    assert square.height == 9
    assert square.area() == 81


def test_square_is_substitutable_by_static_type() -> None:
    square = Square(4)
    assert isinstance(square, Rectangle)
    assert isinstance(square, Shape)
