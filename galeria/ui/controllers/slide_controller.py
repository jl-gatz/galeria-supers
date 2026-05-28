# galeria/ui/controllers/slide_controller.py
"""Controle sequencial de textos exibidos na visão de detalhe."""


class SlideController:
    """Navega por uma lista não vazia de histórias."""

    def __init__(self, historias: list[str]) -> None:
        """Inicializa o controle no primeiro slide."""
        if not historias:
            raise ValueError("historias cannot be empty")
        self._historias = historias
        self._index = 0

    @property
    def index(self) -> int:
        """Retorna o índice do slide atual."""
        return self._index

    @property
    def current(self) -> str:
        """Retorna o texto do slide atual."""
        return self._historias[self._index]

    def next(self) -> bool:
        """Avança um slide quando possível."""
        if self._index < len(self._historias) - 1:
            self._index += 1
            return True
        return False

    def prev(self) -> bool:
        """Retrocede um slide quando possível."""
        if self._index > 0:
            self._index -= 1
            return True
        return False

    def goto(self, index: int) -> bool:
        """Move para um índice específico quando ele existe."""
        if 0 <= index < len(self._historias):
            self._index = index
            return True
        return False
