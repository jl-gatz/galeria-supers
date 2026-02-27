from dataclasses import dataclass


@dataclass
class ScrollState:
    pixels: float
    max_extent: float


class GaleriaController:
    def __init__(self, tolerance: float = 5.0):
        self._tolerance = tolerance

    def should_reset_scroll(self, state: ScrollState) -> bool:
        return state.pixels >= state.max_extent - self._tolerance
