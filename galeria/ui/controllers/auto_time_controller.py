import asyncio
from collections.abc import Callable


class AutoTimeoutController:
    def __init__(self, seconds: int, on_timeout: Callable[[], None]):
        self.seconds = seconds
        self.on_timeout = on_timeout
        self._task: asyncio.Task | None = None

    def start(self):
        self.cancel()
        self._task = asyncio.create_task(self._run())

    def restart(self):
        self.start()

    def cancel(self):
        if self._task and not self._task.done():
            self._task.cancel()
        self._task = None

    async def _run(self):
        try:
            await asyncio.sleep(self.seconds)
            self.on_timeout()
        except asyncio.CancelledError:
            pass
