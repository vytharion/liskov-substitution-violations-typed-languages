from __future__ import annotations

from shapes.shape import Rectangle


class BoundedRectangle(Rectangle):
    def __init__(self, width: float, height: float, max_side: float) -> None:
        super().__init__(width, height)
        self._max_side = max_side

    @property
    def max_side(self) -> float:
        return self._max_side

    def set_width(self, width: float) -> None:
        self._reject_out_of_range(width)
        super().set_width(width)

    def set_height(self, height: float) -> None:
        self._reject_out_of_range(height)
        super().set_height(height)

    def _reject_out_of_range(self, value: float) -> None:
        if value <= 0 or value > self._max_side:
            raise ValueError(
                f"side {value} outside permitted range (0, {self._max_side}]"
            )
