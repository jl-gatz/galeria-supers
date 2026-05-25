from galeria.domain.models import Era
from galeria.domain.services import SuperService
from tests.stubs.fake_repo import FakeSuperRepository


def test_super_service_exposes_eras_from_repository():
    era = Era(
        id="detic",
        nome="Era DETIC",
        periodo="2021-presente",
        ano_inicio=2021,
        ano_final=None,
        theme="detic_era",
        descricao="",
    )
    service = SuperService(repository=FakeSuperRepository(eras=[era]))

    assert service.listar_eras() == [era]
    assert service.obter_era("detic") == era
    assert service.obter_theme_da_era("detic") == "detic_era"
