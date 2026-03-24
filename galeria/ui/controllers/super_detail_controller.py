from galeria.ui.controllers import SlideController


class SuperDetailController:
    def __init__(self, super_data):
        # mantém compatível com o que você já usa
        self._super = super_data
        self._slides = SlideController(super_data.historias)

    @property
    def current(self) -> str:
        return self._slides.current

    def next(self) -> bool:
        return self._slides.next()

    def prev(self) -> bool:
        return self._slides.prev()

    def goto(self, index: int) -> bool:
        return self._slides.goto(index)
