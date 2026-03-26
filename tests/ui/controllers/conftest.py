from collections.abc import Callable

import pytest

from galeria.domain.protocols.super_like import SuperLike
from galeria.ui.controllers.super_detail_controller import SuperDetailController
from tests.stubs.fake_super import FakeSuper


@pytest.fixture
def make_super() -> Callable[[list[str]], SuperLike]:
    def _make(historias: list[str]) -> SuperLike:
        return FakeSuper(historias)

    return _make


@pytest.fixture
def make_controller(make_super: Callable[[list[str]], SuperLike]):
    def _make(historias: list[str]):
        super_data: SuperLike = make_super(historias)
        return SuperDetailController(super_data)

    return _make
