# tests/fakes/fake_repo.py

from galeria.domain.models import Era, Super
from galeria.domain.super_repository import InterfaceSuperRepository


class FakeSuperRepository(InterfaceSuperRepository):
    def __init__(self, supers=None, eras=None):
        self._supers = supers or []
        self._eras = eras or []

    def listar(self) -> list[Super]:
        return self._supers

    def obter_por_id(self, super_id: str) -> Super | None:
        for s in self._supers:
            if getattr(s, "id", None) == super_id:
                return s
        return None

    def listar_eras(self) -> list[Era]:
        return self._eras

    def obter_era(self, era_id: str) -> Era | None:
        for era in self._eras:
            if era.id == era_id:
                return era
        return None

    def obter_theme_da_era(self, era_id: str) -> str | None:
        era = self.obter_era(era_id)
        return era.theme if era else None
