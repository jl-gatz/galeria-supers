# tests/conftest.py
import asyncio

import pytest

from tests.harness.flet_harness import FletTestHarness


@pytest.fixture
def harness():
    return FletTestHarness()


@pytest.fixture(scope="session")
def event_loop():
    """
    Cria um event loop para todos os testes.
    Necessário para componentes Flet.
    """

    loop = asyncio.new_event_loop()
    yield loop
    loop.close()
