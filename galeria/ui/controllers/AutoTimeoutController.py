import asyncio
from collections.abc import Callable


class AutoTimeoutController:
    def __init__(self, seconds: int, on_timeout: Callable[[], None]):
        self.seconds = seconds
        self.on_timeout = on_timeout
        self._task: asyncio.Task | None = None
        self._active = False

    def start(self):
        self.cancel()
        self._active = True
        self._task = asyncio.create_task(self._run())

    def restart(self):
        if self._active:
            self.start()

    def cancel(self):
        self._active = False
        if self._task and not self._task.done():
            self._task.cancel()
        self._task = None

    async def _run(self):
        try:
            await asyncio.sleep(self.seconds)
            if self._active:
                self.on_timeout()
        except asyncio.CancelledError:
            pass
