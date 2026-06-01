from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, Union, final, runtime_checkable


@runtime_checkable
class Shape(Protocol):
    def area(self) -> float: ...


@final
@dataclass(frozen=True)
class Rectangle:
    # Immutability removes the setter surface that Step 1's Square subclass
    # silently rewired. There is no set_width / set_height to override, so
    # no subclass can install a coupled-setter invariant behind the caller's
    # back. A "resize" is a new value, not a hidden mutation.
    width: float
    height: float

    def __post_init__(self) -> None:
        _reject_non_positive(self.width, "width")
        _reject_non_positive(self.height, "height")

    def area(self) -> float:
        return self.width * self.height

    def with_width(self, width: float) -> "Rectangle":
        return Rectangle(width, self.height)

    def with_height(self, height: float) -> "Rectangle":
        return Rectangle(self.width, height)


@final
@dataclass(frozen=True)
class Square:
    # Square is a sibling of Rectangle, NOT a subclass. The naive "a square
    # is-a rectangle" claim is true geometrically and false behaviourally;
    # making it a structural sibling that satisfies the Shape protocol
    # without inheriting Rectangle's setters removes the substitutability
    # trap at the type level.
    side: float

    def __post_init__(self) -> None:
        _reject_non_positive(self.side, "side")

    def area(self) -> float:
        return self.side * self.side

    def with_side(self, side: float) -> "Square":
        return Square(side)


SealedShape = Union[Rectangle, Square]


def total_area(shapes: list[SealedShape]) -> float:
    return sum(shape.area() for shape in shapes)


def _reject_non_positive(value: float, name: str) -> None:
    if value <= 0:
        raise ValueError(f"{name} must be positive, got {value}")
