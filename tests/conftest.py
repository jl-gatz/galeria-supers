# tests/conftest.py

import asyncio
from collections.abc import Generator
from pathlib import Path

import pytest

from galeria.domain import Super, SuperService
from galeria.domain.protocols.super_service_like import SuperServiceLike
from tests.harness import FletTestHarness
from tests.stubs.builders import super_stub_one
from tests.stubs.fake_page import FakePage
from tests.stubs.fake_repo import FakeSuperRepository
from tests.stubs.fake_root import FakeRoot
from tests.stubs.fake_super_service import FakeSuperService
from tests.stubs.fake_theme import FakeTheme
from tests.stubs.fake_theme_manager import FakeThemeManager


# === HARNESSES / INFRA DE TESTE (UI) =========================
@pytest.fixture
def fake_page() -> FakePage:
    """Página fake para componentes Flet"""
    return FakePage()


@pytest.fixture
def fake_root(fake_page: FakePage) -> FakeRoot:
    """Root fake para overlays e navegação"""
    return FakeRoot(fake_page)


@pytest.fixture
def harness(fake_page: FakePage) -> FletTestHarness:
    """Harness para montar componentes Flet"""
    return FletTestHarness(fake_page)


@pytest.fixture
def fake_theme() -> FakeTheme:
    """Theme fake para overlays e navegação"""
    return FakeTheme()


@pytest.fixture
def fake_theme_manager(fake_theme: FakeTheme) -> FakeThemeManager:
    return FakeThemeManager(theme=fake_theme)


# === EVENT LOOP (FLET / ASYNC) ===============================
@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """
    Event loop global para testes (necessário para Flet).
    """
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


# === DADOS DE DOMÍNIO ========================================
@pytest.fixture
def supers_sample() -> list[Super]:
    """Dataset padrão de supers para testes"""
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
            id="",
            nome="_blank",
            foto=None,
            timeline=None,
            timeline_points=None,
            historias=None,
        ),
    ]


# === REPOSITORIES / SERVICES REAIS ===========================
@pytest.fixture
def service(supers_sample: list[Super]) -> SuperService:
    """Service real com repositório fake"""
    repo = FakeSuperRepository(supers_sample)
    return SuperService(repository=repo)


# === STUBS / FAKES DE ALTO NÍVEL =============================
@pytest.fixture
def fake_service() -> SuperServiceLike:
    """
    Service totalmente fake (controle total nos testes de view)
    """
    supers = [
        super_stub_one(nome="Ada", foto="ada.png", timeline="ada.json"),
        super_stub_one(nome="Alan", foto="alan.png", timeline="alan.json"),
        super_stub_one(nome="Bell", foto="bell.png"),
        super_stub_one(nome="_blank", foto=None),
    ]
    return FakeSuperService(supers)
