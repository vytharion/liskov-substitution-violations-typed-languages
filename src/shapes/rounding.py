from __future__ import annotations

from shapes.shape import Rectangle


class RoundingRectangle(Rectangle):
    # Postcondition weakening: the parent promises that after set_width(w),
    # self.width == w. We round to the nearest integer for grid snapping,
    # so the stored value silently drifts from the value the caller supplied.
    def __init__(self, width: float, height: float) -> None:
        super().__init__(round(width), round(height))

    def set_width(self, width: float) -> None:
        super().set_width(round(width))

    def set_height(self, height: float) -> None:
        super().set_height(round(height))
