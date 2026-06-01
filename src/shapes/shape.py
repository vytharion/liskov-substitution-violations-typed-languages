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


class PositiveRectangle(Rectangle):
    # Precondition strengthening: the parent accepts any float, this subclass
    # rejects zero and negatives. Callers written against Rectangle that pass
    # 0 or a negative value will start raising ValueError here.
    def __init__(self, width: float, height: float) -> None:
        self._require_positive(width, "width")
        self._require_positive(height, "height")
        super().__init__(width, height)

    def set_width(self, width: float) -> None:
        self._require_positive(width, "width")
        super().set_width(width)

    def set_height(self, height: float) -> None:
        self._require_positive(height, "height")
        super().set_height(height)

    @staticmethod
    def _require_positive(value: float, name: str) -> None:
        if value <= 0:
            raise ValueError(f"{name} must be positive, got {value}")
