# infrastructure/repositories/super_repository.py

import json

from core.paths import SUPERS_JSON
from domain.models import Super

from galeria.domain.super_repository import InterfaceSuperRepository


class SuperRepository(InterfaceSuperRepository):
    def listar(self) -> list[Super]:
        with open(SUPERS_JSON, encoding="utf-8") as f:
            raw = json.load(f)

        return [
            Super(
                id=s["id"],
                nome=s["nome"],
                foto=s["foto"],
                historias=s["historias"],
            )
            for s in raw
        ]

    def obter_por_id(self, super_id: str) -> Super | None:
        raw = self.listar()

        return [
            Super(
                id=v["id"],
                nome=v["nome"],
                foto=v["foto"],
                historias=v["historias"],
            )
            for k, v in raw.items()
            if k == super_id
        ]
