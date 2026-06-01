from __future__ import annotations

from abc import ABC, abstractmethod


class Shape(ABC):
    @abstractmethod
    def area(self) -> float:
        ...


class Rectangle(Shape):
    def __init__(self, width: float, height: float) -> None:
        self._width = width
        self._height = height

    @property
    def width(self) -> float:
        return self._width

    @property
    def height(self) -> float:
        return self._height

    def set_width(self, width: float) -> None:
        self._width = width

    def set_height(self, height: float) -> None:
        self._height = height

    def area(self) -> float:
        return self._width * self._height


class Square(Rectangle):
    def __init__(self, side: float) -> None:
        super().__init__(side, side)

    # Hidden coupling: writing one dimension silently rewrites the other
    # to preserve the square invariant width == height.
    def set_width(self, width: float) -> None:
        self._width = width
        self._height = width

    def set_height(self, height: float) -> None:
        self._width = height
        self._height = height
