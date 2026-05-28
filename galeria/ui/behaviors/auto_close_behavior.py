# galeria/ui/behaviors/auto_close_behavior.py
"""Comportamento de autofechamento para controles temporários."""

from collections.abc import Callable

from galeria.ui.controllers import AutoTimeoutController


class AutoCloseBehavior:
    """Fachada simples para iniciar, reiniciar e cancelar timeout de fechamento."""

    def __init__(self, seconds: int, on_timeout: Callable[[], None]):
        """Configura o tempo de espera e a ação disparada no timeout."""
        self._controller = AutoTimeoutController(
            seconds=seconds,
            on_timeout=on_timeout,
        )

    def start(self) -> None:
        """Inicia a contagem para fechamento automático."""
        self._controller.start()

    def reset(self) -> None:
        """Reinicia a contagem após uma nova interação do usuário."""
        self._controller.restart()

    def stop(self) -> None:
        """Cancela a contagem ativa de fechamento automático."""
        self._controller.cancel()
