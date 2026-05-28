# galeria/ui/components/timeline/view/timeline_canvas.py
"""Wrapper leve para o canvas usado pela timeline."""

from typing import Any, cast

import flet.canvas as cv


class TimelineCanvas:
    """Mantém o canvas Flet e expõe dimensões usadas no desenho."""

    def __init__(self, on_resize: Any | None = None):
        self.canvas = cv.Canvas(shapes=[], expand=True, width=1900, height=300, on_resize=on_resize)

    @property
    def width(self) -> float:
        """Retorna a largura atual do canvas."""
        return cast(float, self.canvas.width)

    @property
    def height(self) -> float:
        """Retorna a altura atual do canvas."""
        return cast(float, self.canvas.height)

    def set_shapes(self, shapes: list[Any]) -> None:
        """Substitui as formas desenhadas no canvas."""
        self.canvas.shapes = shapes
