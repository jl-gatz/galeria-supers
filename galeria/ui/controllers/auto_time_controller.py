# galeria/ui/controllers/auto_time_controller.py
"""Controle assíncrono de timeout reiniciável."""

import asyncio
from collections.abc import Callable, Coroutine
from typing import Any, override


class AutoTimeoutController:
    """Dispara uma ação após inatividade, com suporte a reset e cancelamento."""

    def __init__(
        self,
        seconds: float,
        on_timeout: Callable[[], None],
        scheduler: Callable[[Coroutine[Any, Any, None]], asyncio.Task[None]] | None = None,
    ):
        """Configura duração, callback e scheduler opcional para testes."""
        self.seconds = seconds
        self.on_timeout = on_timeout
        self.scheduler = scheduler

        self._task: asyncio.Task[None] | None = None
        self._token = 0

    # ---------------------------------------------------------
    # lifecycle
    # ---------------------------------------------------------

    def start(self):
        """Inicia uma nova task de timeout, cancelando a anterior."""

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
        """Reinicia o contador de inatividade."""
        self.start()

    def cancel(self):
        """Cancela a task de timeout atual."""
        if self._task and not self._task.done():
            self._task.cancel()

        self._task = None

    # ---------------------------------------------------------
    # coroutine
    # ---------------------------------------------------------

    async def _run(self, token: int):
        """Aguarda o período configurado e executa o callback vigente."""

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
        """Indica se há um timeout ativo."""
        return self._task is not None and not self._task.done()

    @override
    def __repr__(self) -> str:
        """Retorna uma representação textual do estado do controller."""

        state = "running" if self.running else "stopped"

        return f"<AutoTimeoutController {state} ({self.seconds}s)>"
