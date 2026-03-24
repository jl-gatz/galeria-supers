# tests/fakes/fake_repo.py

from galeria.domain.models import Super
from galeria.domain.super_repository import InterfaceSuperRepository


class FakeSuperRepository(InterfaceSuperRepository):
    def __init__(self, supers=None):
        self._supers = supers or []

    def listar(self) -> list[Super]:
        return self._supers

    def obter_por_id(self, super_id: str) -> Super | None:
        for s in self._supers:
            if getattr(s, "id", None) == super_id:
                return s
        return None
