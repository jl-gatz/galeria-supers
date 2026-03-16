import asyncio
from collections.abc import Callable, Coroutine


class AutoTimeoutController:
    """
    Controller responsável por disparar uma ação após um período de inatividade.

    Características:
    - reiniciável
    - cancelável
    - compatível com asyncio
    - testável via scheduler injetado
    """

    def __init__(
        self,
        seconds: float,
        on_timeout: Callable[[], None],
        scheduler: Callable[[Coroutine], asyncio.Task] | None = None,
    ):
        """
        Parameters
        ----------
        seconds:
            tempo de espera antes do timeout
        on_timeout:
            callback executado após timeout
        scheduler:
            função responsável por criar a task (usado para testes)
        """
        self.seconds = seconds
        self.on_timeout = on_timeout
        self.scheduler = scheduler

        self._task: asyncio.Task | None = None
        self._token = 0

    # ---------------------------------------------------------
    # lifecycle
    # ---------------------------------------------------------

    def start(self):

        self.cancel()

        self._token += 1
        token = self._token

        coro = self._run(token)

        if self.scheduler:
            self._task = self.scheduler(coro)
            return

        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.get_event_loop()

        self._task = loop.create_task(coro)

    def restart(self):
        """
        Reinicia o contador.
        """
        self.start()

    def cancel(self):
        """
        Cancela o timeout atual.
        """
        if self._task and not self._task.done():
            self._task.cancel()

        self._task = None

    # ---------------------------------------------------------
    # coroutine
    # ---------------------------------------------------------

    async def _run(self, token: int):

        try:
            await asyncio.sleep(self.seconds)

            # garante que só a task mais recente execute
            if token != self._token:
                return

            try:
                self.on_timeout()
            except Exception:
                import logging

                logging.exception("AutoTimeoutController callback error")

        except asyncio.CancelledError:
            pass

    # ---------------------------------------------------------
    # helpers
    # ---------------------------------------------------------

    @property
    def running(self):
        """
        Indica se o timer está ativo.
        """
        return self._task is not None and not self._task.done()

    def __repr__(self):

        state = "running" if self.running else "stopped"

        return f"<AutoTimeoutController {state} ({self.seconds}s)>"
