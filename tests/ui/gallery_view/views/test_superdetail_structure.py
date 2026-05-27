from unittest.mock import Mock

import pytest

from galeria.ui.components.super_header import SuperHeader
from galeria.ui.views.super_view import SuperDetail
from tests.factories import SuperDetailFactory
from tests.harness import FletTestHarness


@pytest.mark.asyncio
async def test_superdetail_mounts(
    harness: FletTestHarness,
    super_detail: SuperDetail,
):
    """
    Verifica se SuperDetail monta corretamente.
    """

    await harness.mount(super_detail)

    assert harness.count("SuperDetail") == 1


@pytest.mark.asyncio
async def test_superdetail_has_header(
    harness: FletTestHarness,
    super_detail: SuperDetail,
):
    """
    Verifica se SuperHeader está presente na árvore.
    """

    await harness.mount(super_detail)

    headers = harness.find(SuperHeader)

    assert len(headers) == 1


def test_superdetail_timeline_callback_updates_header():
    detail = SuperDetailFactory.build(
        auto_start=False,
        timeline_points=[
            {
                "id": "ingresso",
                "year": 1967,
                "label": "Ingresso",
                "x": 0.1,
                "y": 0.8,
                "text": "Alfredo inicia sua trajetória.",
            }
        ],
    )
    detail.auto_close.reset = Mock()

    detail.timeline_view.controller.select_point("ingresso")

    assert [control.value for control in detail.header.text_list.controls[:3]] == [
        "1967",
        "Ingresso",
        "Alfredo inicia sua trajetória.",
    ]


@pytest.mark.asyncio
async def test_superheader_is_descendant_of_superdetail(
    harness: FletTestHarness,
    super_detail: SuperDetail,
):
    """
    Verifica se SuperHeader pertence à árvore do SuperDetail.
    """

    await harness.mount(super_detail)

    detail = harness.one("SuperDetail")

    headers = harness.find_descendants(
        detail,
        "SuperHeader",
    )

    assert len(headers) == 1
