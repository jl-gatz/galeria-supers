# tests/fakes/fake_repo.py

from collections.abc import Sequence
from typing import override

from galeria.domain.models import Era, Super
from galeria.domain.super_repository import InterfaceSuperRepository


class FakeSuperRepository(InterfaceSuperRepository):
    def __init__(self, supers: Sequence[Super] | None = None, eras: Sequence[Era] | None = None):
        self._supers = list(supers or [])
        self._eras = list(eras or [])

    @override
    def listar(self) -> list[Super]:
        return self._supers

    @override
    def obter_por_id(self, super_id: str) -> Super | None:
        for s in self._supers:
            if s.id == super_id:
                return s
        return None

    @override
    def listar_eras(self) -> list[Era]:
        return self._eras

    @override
    def obter_era(self, era_id: str) -> Era | None:
        for era in self._eras:
            if era.id == era_id:
                return era
        return None

    @override
    def obter_theme_da_era(self, era_id: str) -> str | None:
        era = self.obter_era(era_id)
        return era.theme if era else None
