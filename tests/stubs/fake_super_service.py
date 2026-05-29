from collections.abc import Callable, Sequence
from pathlib import Path

from galeria.domain.models import Era, Super


def _default_pode_abrir(super_data: Super) -> bool:
    return super_data.nome != "_blank"


def _default_image_path(super_data: Super) -> Path | None:
    if super_data.foto is None:
        return None
    return Path(f"/fake/images/{super_data.foto}")


def _default_timeline_path(super_data: Super) -> Path | None:
    if super_data.timeline is None:
        return None
    return Path(f"/fake/timeline/{super_data.timeline}")


class FakeSuperService:
    def __init__(
        self,
        supers: Sequence[Super],
        pode_abrir_fn: Callable[[Super], bool] | None = None,
        image_path_fn: Callable[[Super], Path | None] | None = None,
        timeline_path_fn: Callable[[Super], Path | None] | None = None,
        eras: Sequence[Era] | None = None,
    ):
        self._supers = list(supers)
        self._eras = list(eras or [])

        # comportamento padrão (simples e previsível)
        self._pode_abrir_fn: Callable[[Super], bool] = pode_abrir_fn or _default_pode_abrir
        self._image_path_fn: Callable[[Super], Path | None] = image_path_fn or _default_image_path
        self._timeline_path_fn: Callable[[Super], Path | None] = (
            timeline_path_fn or _default_timeline_path
        )

    # ==========================================
    # Interface esperada pelo GalleryView
    # ==========================================
    def listar_supers(self) -> Sequence[Super]:
        return self._supers

    def listar_eras(self) -> Sequence[Era]:
        return self._eras

    def obter_era(self, era_id: str) -> Era | None:
        return next((era for era in self._eras if era.id == era_id), None)

    def obter_theme_da_era(self, era_id: str) -> str | None:
        era = self.obter_era(era_id)
        return era.theme if era else None

    def pode_abrir(self, super_data: Super) -> bool:
        return self._pode_abrir_fn(super_data)

    def build_image_path(self, super_data: Super) -> Path | None:
        return self._image_path_fn(super_data)

    def build_timeline_path(self, super_data: Super) -> Path | None:
        return self._timeline_path_fn(super_data)

    def is_blank(self, super_data: Super) -> bool:
        return super_data.nome == "_blank"
