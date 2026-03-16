import asyncio

import pytest

from galeria.ui.controllers.auto_time_controller import AutoTimeoutController


@pytest.mark.asyncio
async def test_timeout_trigger():

    triggered = False

    def on_timeout():
        nonlocal triggered
        triggered = True

    controller = AutoTimeoutController(seconds=0.01, on_timeout=on_timeout)

    controller.start()

    await asyncio.sleep(0.02)

    assert triggered
