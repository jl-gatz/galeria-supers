import json
from pathlib import Path

from galeria.infrastructure.repositories.super_repository import SuperRepository


def _write_json(path: Path, data):
    path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")


def _super_payload(super_id: int, nome: str, foto: str = "ada__gray.png"):
    return {
        "id": super_id,
        "nome": nome,
        "foto": foto,
        "periodo": "1967-1969",
        "timeline": "",
        "timeline_points": [],
        "historias": [],
    }


def test_repository_loads_grouped_supers_and_injects_era_id(tmp_path):
    supers_path = tmp_path / "supers.json"
    eras_path = tmp_path / "eras.json"
    _write_json(
        supers_path,
        {
            "ccuec": [_super_payload(1, "Ada")],
            "detic": [_super_payload(2, "Grace")],
        },
    )
    _write_json(eras_path, {})

    repository = SuperRepository(supers_path=supers_path, eras_path=eras_path)

    supers = repository.listar()

    assert [super_data.nome for super_data in supers] == ["Ada", "Grace"]
    assert [super_data.era_id for super_data in supers] == ["ccuec", "detic"]
    assert supers[0].foto == Path("images/supers/grayscale/ada__gray.png")


def test_repository_supports_legacy_flat_super_list(tmp_path):
    supers_path = tmp_path / "supers.json"
    eras_path = tmp_path / "eras.json"
    detic_super = _super_payload(2, "Grace")
    detic_super["era"] = "detic"
    _write_json(supers_path, [_super_payload(1, "Ada"), detic_super])
    _write_json(eras_path, {})

    repository = SuperRepository(supers_path=supers_path, eras_path=eras_path)

    supers = repository.listar()

    assert [super_data.era_id for super_data in supers] == ["ccuec", "detic"]


def test_repository_loads_eras_and_theme_by_id(tmp_path):
    supers_path = tmp_path / "supers.json"
    eras_path = tmp_path / "eras.json"
    _write_json(supers_path, {})
    _write_json(
        eras_path,
        {
            "ccuec": {
                "id": "ccuec",
                "nome": "Era CCUEC",
                "periodo": "1967-2021",
                "ano_inicio": 1967,
                "ano_final": 2021,
                "theme": "ccuec_era",
                "descricao": "",
            },
            "detic": {
                "id": "detic",
                "nome": "Era DETIC",
                "periodo": "2021-presente",
                "ano_inicio": 2021,
                "ano_final": None,
                "theme": "detic_era",
                "descricao": "",
            },
        },
    )

    repository = SuperRepository(supers_path=supers_path, eras_path=eras_path)

    eras = repository.listar_eras()

    assert [era.id for era in eras] == ["ccuec", "detic"]
    assert repository.obter_era("detic").nome == "Era DETIC"
    assert repository.obter_theme_da_era("ccuec") == "ccuec_era"
    assert repository.obter_theme_da_era("missing") is None
