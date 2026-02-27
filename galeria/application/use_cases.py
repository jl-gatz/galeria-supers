# UseCases eh necessário??
from collections.abc import Sequence

from galeria.domain.models import Super
from galeria.domain.repository import SuperRepository


class ListarSupers:
    def __init__(self, repository: SuperRepository) -> None:
        self._repository = repository

    def executar(self) -> Sequence[Super]:
        return self._repository.listar()


class ObterSuper:
    def __init__(self, repository: SuperRepository) -> None:
        self._repository = repository

    def executar(self, super_id: str) -> Super | None:
        return self._repository.obter_por_id(super_id)
