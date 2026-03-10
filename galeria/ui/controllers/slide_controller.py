# ui/controllers/slide_controller.py
class SlideController:
    def __init__(self, historias: list[str]):
        self._historias = historias
        self._index = 0

    @property
    def index(self) -> int:
        return self._index

    @property
    def current(self) -> str:
        return self._historias[self._index]

    def next(self) -> bool:
        if self._index < len(self._historias) - 1:
            self._index += 1
            return True
        return False

    def prev(self) -> bool:
        if self._index > 0:
            self._index -= 1
            return True
        return False

    def goto(self, index: int) -> bool:
        if 0 <= index < len(self._historias):
            self._index = index
            return True
        return False
