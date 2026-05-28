# galeria/ui/controllers/super_detail_controller.py
"""Adaptador entre dados de domínio e a visão de detalhe."""

from collections.abc import Sequence
from pathlib import Path

from galeria.domain.protocols import SuperLike
from galeria.ui.controllers import SlideController


class SuperDetailController:
    """Expõe dados e navegação de slides para a view de detalhe."""

    def __init__(self, super_data: SuperLike) -> None:
        """Cria o controller a partir de um superintendente."""
        self._super = super_data
        historias = super_data.historias
        self._slides = SlideController(
            list(historias)
            if isinstance(historias, Sequence) and not isinstance(historias, str)
            else [""]
        )

    # -------------------------
    # 🧱 Helpers internos
    # -------------------------
    def _to_src(self, path: Path | str | None) -> str | None:
        """Converte caminhos locais em string compatível com componentes Flet."""
        if path is None:
            return None

        if isinstance(path, Path):
            return path.as_posix()

        return str(path)

    # -------------------------
    # 🎯 Dados para a View
    # -------------------------
    @property
    def nome(self) -> str:
        """Retorna o nome exibido no detalhe."""
        return self._super.nome

    @property
    def periodo(self) -> str | None:
        """Retorna o período exibido abaixo do retrato."""
        return getattr(self._super, "periodo", None)

    @property
    def image_src(self) -> str | None:
        """Retorna a origem da imagem de retrato."""
        return self._to_src(self._super.foto)

    @property
    def timeline_src(self) -> str | None:
        """Retorna a origem da imagem de timeline, quando existir."""
        return self._to_src(self._super.timeline)

    @property
    def timeline_points(self):
        """Retorna os pontos narrativos da timeline."""
        return self._super.timeline_points or []

    # @property
    # def timeline(self) -> dict:
    #     return {
    #         "image_src": self.timeline_src,
    #         "points": self.timeline_points,
    #     }

    # -------------------------
    # 🎞 Slides
    # -------------------------
    @property
    def current(self) -> str:
        """Retorna o texto do slide atual."""
        return self._slides.current

    def next(self) -> bool:
        """Avança para o próximo slide quando possível."""
        return self._slides.next()

    def prev(self) -> bool:
        """Retrocede para o slide anterior quando possível."""
        return self._slides.prev()

    def goto(self, index: int) -> bool:
        """Vai para um slide específico quando o índice é válido."""
        return self._slides.goto(index)

    # def sync_timeline_with_slide(self):
    #     index = self._slides.index  # ou como você controla isso
    #     self._timeline_ctrl.active_index = index
