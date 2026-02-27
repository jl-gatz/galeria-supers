from collections.abc import Sequence
from pathlib import Path
from typing import override

from galeria.domain.models import Super
from galeria.domain.repository import SuperRepository


class InMemorySuperRepository(SuperRepository):
    def __init__(self, assets_path: Path) -> None:
        self._supers: list[Super] = [
            Super(
                id="1",
                nome="Super Python",
                descricao="Mestre das tipagens estritas.",
                foto=assets_path / "super_python.png",
            ),
            Super(
                id="2",
                nome="Capitão Async",
                descricao="Domina o tempo e o event loop.",
                foto=assets_path / "capitao_async.png",
            ),
        ]

    @override
    def listar(self) -> Sequence[Super]:
        return self._supers

    @override
    def obter_por_id(self, super_id: str) -> Super | None:
        for super_obj in self._supers:
            if super_obj.id == super_id:
                return super_obj
        return None
