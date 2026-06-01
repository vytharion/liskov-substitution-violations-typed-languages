from __future__ import annotations

from shapes.shape import Rectangle


class ClampedRectangle(Rectangle):
    def __init__(self, width: float, height: float, max_side: float) -> None:
        self._max_side = max_side
        super().__init__(self._clamp(width), self._clamp(height))

    @property
    def max_side(self) -> float:
        return self._max_side

    def set_width(self, width: float) -> None:
        super().set_width(self._clamp(width))

    def set_height(self, height: float) -> None:
        super().set_height(self._clamp(height))

    def _clamp(self, value: float) -> float:
        if value > self._max_side:
            return self._max_side
        return value
