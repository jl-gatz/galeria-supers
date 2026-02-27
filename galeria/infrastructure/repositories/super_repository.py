# infrastructure/repositories/super_repository.py

import json

from core.paths import SUPERS_JSON
from domain.models import Super


class SuperRepository:
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
