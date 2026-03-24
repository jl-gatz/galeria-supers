# tests/conftest.py
import asyncio
from pathlib import Path
from typing import Any

import pytest

from galeria.domain import Super, SuperService
from tests.harness import FletTestHarness
from tests.stubs import FakePage
from tests.stubs.builders import super_stub_one
from tests.stubs.fake_repo import FakeSuperRepository
from tests.stubs.fake_root import FakeRoot
from tests.stubs.fake_super_service import FakeSuperService


@pytest.fixture
def fake_page():
    """
    Fixture da página falsa para os componentes Flet
    """
    return FakePage()


@pytest.fixture
def fake_root():
    """
    Fixture do falso conf root para os componentes Flet
    """
    return FakeRoot()


@pytest.fixture
def harness(fake_page: Any):
    """
    Retorna o objeto montador de testes
    """
    return FletTestHarness(fake_page)


@pytest.fixture(scope="session")
def event_loop():
    """
    Cria um event loop para todos os testes.
    Necessário para componentes Flet.
    """

    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def supers_sample():
    return [
        Super(
            id="1",
            nome="Ada",
            foto=Path("ada.png"),
            timeline=Path("ada.json"),
            timeline_points=None,
            historias=None,
        ),
        Super(
            id="2",
            nome="Alan",
            foto=Path("turing.png"),
            timeline=Path("turing.json"),
            timeline_points=None,
            historias=None,
        ),
        Super(
            id="3",
            nome="Bell",
            foto=None,
            timeline=None,
            timeline_points=None,
            historias=None,
        ),
        Super(
            id="4",
            nome="_blank",
            foto=None,
            timeline=None,
            timeline_points=None,
            historias=None,
        ),
    ]


@pytest.fixture
def service(supers_sample: list[Super]):
    repo = FakeSuperRepository(supers_sample)
    return SuperService(repository=repo)


@pytest.fixture
def fake_service():
    supers = [
        super_stub_one(nome="Ada", foto="ada.png", timeline="ada.json"),
        super_stub_one(nome="Alan", foto="alan.png", timeline="alan.json"),
        super_stub_one(nome="Bell", foto="bell.png"),
        super_stub_one(nome="_blank", foto=None),
    ]
    return FakeSuperService(supers)
