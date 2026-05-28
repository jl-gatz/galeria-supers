# galeria/ui/components/timeline/controller/timeline_controller.py
"""Controle de animação, seleção e estados dos pontos da timeline."""


import asyncio
import math
from collections.abc import Callable
from typing import Any

from galeria.ui.components.timeline.models import TimelineModel, TimelinePoint


class TimelineController:
    """Coordena progresso animado e seleção narrativa da timeline."""

    def __init__(
        self,
        model: TimelineModel,
        on_point_selected: Callable[[TimelinePoint], None] | None = None,
    ):
        self.model = model
        self.on_point_selected = on_point_selected

        # estado público (consumido pela view)
        self.progress = 0.0
        self.active_index = 0
        self.selected_point_id: str | None = None
        self.clicked_point_ids: set[str] = set()

        # controle interno
        self._animation_done = False
        self._running = False
        self._task: Any | None = None

        self.view: Any | None = None

    # -------------------------
    # binding
    # -------------------------
    def bind_view(self, view: Any) -> None:
        """Associa uma view ao controlador para permitir refresh."""
        self.view = view

    # -------------------------
    # controle da animação
    # -------------------------
    def start(self) -> None:
        """Inicia (ou reinicia) a animação."""
        self.progress = 0.0
        self._animation_done = False
        self._running = True

        self._ensure_loop()

    def stop(self) -> None:
        """Para a animação."""
        self._running = False
        self._animation_done = True

    def reset(self) -> None:
        """Reseta sem iniciar."""
        self.progress = 0.0
        self.active_index = 0
        self._animation_done = False
        self._running = False

        if self.view:
            self.view.refresh()

    # -------------------------
    # loop
    # -------------------------
    def _ensure_loop(self) -> None:
        """Garante que exista um loop de animação ativo na página Flet."""
        if not self.view:
            return

        page = getattr(self.view.control, "page", None)
        if not page:
            return

        # evita múltiplos loops concorrentes
        if self._task:
            return

        self._task = page.run_task(self._loop)

    async def _loop(self) -> None:
        """Executa ticks da animação enquanto o controlador estiver ativo."""
        try:
            while self._running and not self._animation_done:
                self.tick()
                await asyncio.sleep(0.016)  # ~60 FPS
        finally:
            self._task = None

    # -------------------------
    # lógica de animação
    # -------------------------
    def tick(self) -> None:
        """Avança um passo da animação e solicita redesenho da view."""
        if not self._running or self._animation_done:
            return

        # progresso linear
        self.progress = min(1.0, self.progress + 0.02)

        if self.progress >= 1.0:
            self.progress = 1.0
            self._animation_done = True

        # print("TICK:", self.progress)

        self._update_active_index()

        if self.view:
            self.view.refresh()

    def _update_active_index(self) -> None:
        """Atualiza o índice ativo a partir do progresso da animação."""
        total = len(self.model.points)

        if total <= 1:
            self.active_index = 0
            return

        self.active_index = int(self.progress * (total - 1))

    # -------------------------
    # seleção narrativa
    # -------------------------
    def select_point(self, point_id: str) -> TimelinePoint | None:
        """Seleciona um ponto, marca-o como visitado e emite callback."""
        # print(
        #     "TIMELINE CONTROLLER SELECT:",
        #     f"requested={point_id}",
        #     f"available={[point.id for point in self.model.points]}",
        # )
        point = self.model.get_point_by_id(point_id)
        if point is None:
            # print("TIMELINE CONTROLLER SELECT MISS:", point_id)
            return None

        self.selected_point_id = point.id
        self.clicked_point_ids.add(point.id)
        self.active_index = self.model.points.index(point)
        # print(
        #     "TIMELINE CONTROLLER STATE:",
        #     f"selected={self.selected_point_id}",
        #     f"clicked={sorted(self.clicked_point_ids)}",
        #     f"active_index={self.active_index}",
        # )

        if self.on_point_selected:
            # print("TIMELINE CONTROLLER CALLBACK:", point.id)
            self.on_point_selected(point)
        else:
            # print("TIMELINE CONTROLLER CALLBACK: none")
            pass

        return point

    def point_state(self, point_id: str) -> str:
        """Retorna o estado visual de um ponto pelo identificador."""
        if point_id == self.selected_point_id:
            return "selected"

        if point_id in self.clicked_point_ids:
            return "clicked"

        return "normal"

    def point_states(self) -> dict[int, str]:
        """Retorna estados visuais indexados para consumo pelo renderer."""
        states: dict[int, str] = {}

        for index, point in enumerate(self.model.points):
            if point.id in self.clicked_point_ids:
                states[index] = "clicked"

            if point.id == self.selected_point_id:
                states[index] = "selected"

        return states

    # -------------------------
    # easing (opcional)
    # -------------------------
    def get_eased_progress(self) -> float:
        """Retorna o progresso com easing sem alterar o estado interno."""
        return 0.5 - 0.5 * math.cos(self.progress * math.pi)
