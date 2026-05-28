# galeria/infrastructure/repositories/super_repository.py
"""Repositório JSON de superintendentes e eras."""

import json
from pathlib import Path
from typing import Any, cast, override

from galeria.core import ERAS_JSON, IMAGES_URL, SUPERS_JSON
from galeria.domain import Era, InterfaceSuperRepository, Super


class SuperRepository(InterfaceSuperRepository):
    """Carrega dados de domínio a partir dos arquivos JSON da aplicação."""

    def __init__(
        self,
        supers_path: Path = SUPERS_JSON,
        eras_path: Path = ERAS_JSON,
        default_era_id: str = "ccuec",
    ):
        """Configura caminhos de dados e era padrão para registros legados."""
        self.supers_path = supers_path
        self.eras_path = eras_path
        self.default_era_id = default_era_id

    @override
    def listar(self) -> list[Super]:
        """Lista superintendentes em formato plano, preservando a era."""
        raw = self._load_json(self.supers_path)
        return [
            self._build_super(super_data, era_id)
            for era_id, supers in self._iter_supers_by_era(raw)
            for super_data in supers
        ]

    @override
    def obter_por_id(self, super_id: str) -> Super | None:
        """Obtém um superintendente pelo identificador."""
        return next((super_data for super_data in self.listar() if super_data.id == super_id), None)

    @override
    def listar_eras(self) -> list[Era]:
        """Lista todas as eras cadastradas no JSON de eras."""
        raw = self._load_json(self.eras_path)
        return [self._build_era(era_data) for era_data in raw.values()]

    @override
    def obter_era(self, era_id: str) -> Era | None:
        """Obtém uma era pelo identificador."""
        return next((era for era in self.listar_eras() if era.id == era_id), None)

    @override
    def obter_theme_da_era(self, era_id: str) -> str | None:
        """Retorna o identificador de tema associado à era."""
        era = self.obter_era(era_id)
        return era.theme if era else None

    def _load_json(self, path: Path) -> Any:
        """Lê um arquivo JSON usando UTF-8."""
        with open(path, encoding="utf-8") as f:
            return json.load(f)

    def _iter_supers_by_era(self, raw: Any) -> list[tuple[str, list[dict[str, Any]]]]:
        """Normaliza dados legados ou agrupados por era."""
        if isinstance(raw, list):
            flat_supers = cast(list[dict[str, Any]], raw)
            return [
                (
                    self._era_id_from_flat_super(super_data),
                    [super_data],
                )
                for super_data in flat_supers
            ]

        grouped_supers = cast(dict[str, list[dict[str, Any]]], raw)
        return [(era_id, supers) for era_id, supers in grouped_supers.items()]

    def _era_id_from_flat_super(self, super_data: dict[str, Any]) -> str:
        """Resolve a era de um registro em formato plano."""
        return str(
            super_data.get("era_id")
            or super_data.get("era")
            or self.default_era_id
        )

    def _build_super(self, super_data: dict[str, Any], era_id: str) -> Super:
        """Converte um dicionário bruto em entidade Super."""
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
        """Converte um dicionário bruto em entidade Era."""
        return Era(
            id=era_data["id"],
            nome=era_data["nome"],
            periodo=era_data["periodo"],
            ano_inicio=era_data["ano_inicio"],
            ano_final=era_data["ano_final"],
            theme=era_data["theme"],
            descricao=era_data.get("descricao", ""),
        )
