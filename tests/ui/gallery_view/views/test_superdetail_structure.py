import pytest

from galeria.ui.components.super_header import SuperHeader
from galeria.ui.views.super_view import SuperDetail
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
