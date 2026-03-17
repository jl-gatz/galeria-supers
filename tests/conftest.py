# tests/conftest.py
import asyncio
from typing import Any

import pytest

from tests.harness import FletTestHarness
from tests.stubs import FakePage


@pytest.fixture
def fake_page():
    """
    Fixture da página falsa para os componentes Flet
    """
    return FakePage()


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
