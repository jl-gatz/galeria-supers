# ui/controllers/super_detail_controller.py

from pathlib import Path

from galeria.domain.protocols import SuperLike
from galeria.ui.controllers import SlideController


class SuperDetailController:
    def __init__(self, super_data: SuperLike) -> None:
        self._super = super_data
        self._slides = SlideController(super_data.historias)

    # -------------------------
    # 🧱 Helpers internos
    # -------------------------
    def _to_src(self, path: Path | str | None) -> str | None:
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
        return self._super.nome

    @property
    def periodo(self) -> str | None:
        return getattr(self._super, "periodo", None)

    @property
    def image_src(self) -> str | None:
        return self._to_src(self._super.foto)

    @property
    def timeline_src(self) -> str | None:
        return self._to_src(self._super.timeline)

    @property
    def timeline_points(self):
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
        return self._slides.current

    def next(self) -> bool:
        return self._slides.next()

    def prev(self) -> bool:
        return self._slides.prev()

    def goto(self, index: int) -> bool:
        return self._slides.goto(index)

    # def sync_timeline_with_slide(self):
    #     index = self._slides.index  # ou como você controla isso
    #     self._timeline_ctrl.active_index = index
