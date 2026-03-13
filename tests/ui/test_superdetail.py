import pytest

from galeria.ui.components.super_header import SuperHeader
from galeria.ui.views.super_view import SuperDetail
from tests.harness.flet_harness import FletTestHarness


@pytest.mark.asyncio
async def test_superdetail_structure(harness: FletTestHarness, super_detail: SuperDetail):
    # await asyncio.sleep(0)
    await harness.mount(super_detail)

    # DEBUG
    harness.debug_tree()

    headers = harness.find(SuperHeader)

    assert len(headers) == 1
