# infrastructure/repositories/super_repository.py

import json
from pathlib import Path
from typing import Any, override

from galeria.core import ERAS_JSON, IMAGES_URL, SUPERS_JSON
from galeria.domain import Era, InterfaceSuperRepository, Super


class SuperRepository(InterfaceSuperRepository):
    def __init__(
        self,
        supers_path: Path = SUPERS_JSON,
        eras_path: Path = ERAS_JSON,
        default_era_id: str = "ccuec",
    ):
        self.supers_path = supers_path
        self.eras_path = eras_path
        self.default_era_id = default_era_id

    @override
    def listar(self) -> list[Super]:
        raw = self._load_json(self.supers_path)
        return [
            self._build_super(super_data, era_id)
            for era_id, supers in self._iter_supers_by_era(raw)
            for super_data in supers
        ]

    @override
    def obter_por_id(self, super_id: str) -> Super | None:
        return next((super_data for super_data in self.listar() if super_data.id == super_id), None)

    @override
    def listar_eras(self) -> list[Era]:
        raw = self._load_json(self.eras_path)
        return [self._build_era(era_data) for era_data in raw.values()]

    @override
    def obter_era(self, era_id: str) -> Era | None:
        return next((era for era in self.listar_eras() if era.id == era_id), None)

    @override
    def obter_theme_da_era(self, era_id: str) -> str | None:
        era = self.obter_era(era_id)
        return era.theme if era else None

    def _load_json(self, path: Path) -> Any:
        with open(path, encoding="utf-8") as f:
            return json.load(f)

    def _iter_supers_by_era(self, raw: Any) -> list[tuple[str, list[dict[str, Any]]]]:
        if isinstance(raw, list):
            return [
                (
                    self._era_id_from_flat_super(super_data),
                    [super_data],
                )
                for super_data in raw
            ]

        return [(era_id, supers) for era_id, supers in raw.items()]

    def _era_id_from_flat_super(self, super_data: dict[str, Any]) -> str:
        return str(
            super_data.get("era_id")
            or super_data.get("era")
            or self.default_era_id
        )

    def _build_super(self, super_data: dict[str, Any], era_id: str) -> Super:
        foto = super_data.get("foto")
        timeline = super_data.get("timeline")
        return Super(
            id=str(super_data["id"]),
            nome=super_data["nome"],
            foto=IMAGES_URL / foto if foto else None,
            timeline=Path(timeline) if timeline else None,
            timeline_points=super_data.get("timeline_points"),
            historias=super_data.get("historias"),
            periodo=super_data.get("periodo"),
            era_id=era_id,
        )

    def _build_era(self, era_data: dict[str, Any]) -> Era:
        return Era(
            id=era_data["id"],
            nome=era_data["nome"],
            periodo=era_data["periodo"],
            ano_inicio=era_data["ano_inicio"],
            ano_final=era_data["ano_final"],
            theme=era_data["theme"],
            descricao=era_data.get("descricao", ""),
        )
