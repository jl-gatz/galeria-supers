# infrastructure/repositories/super_repository.py

import json
from typing import override

from galeria.core import IMAGES_URL, SUPERS_JSON
from galeria.domain import InterfaceSuperRepository, Super


class SuperRepository(InterfaceSuperRepository):
    @override
    def listar(self) -> list[Super]:
        with open(SUPERS_JSON, encoding="utf-8") as f:
            raw = json.load(f)

        return [
            Super(
                id=s["id"],
                nome=s["nome"],
                foto=IMAGES_URL / s["foto"],
                timeline=s["timeline"],
                timeline_points=s["timeline_points"],
                historias=s["historias"],
                periodo=s.get("periodo"),
            )
            for s in raw
        ]

    @override
    def obter_por_id(self, super_id: str) -> Super | None:
        raw = self.listar()

        return [
            Super(
                id=v["id"],
                nome=v["nome"],
                foto=v["foto"],
                timeline=v["timeline"],
                timeline_points=v["timeline_points"],
                historias=v["historias"],
                periodo=v.get("periodo"),
            )
            for k, v in raw.items()
            if k == super_id
        ]
