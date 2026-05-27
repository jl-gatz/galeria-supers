# galeria/ui/components/timeline/controller/timeline_controller.py


import asyncio
import math
from collections.abc import Callable


class TimelineController:
    def __init__(self, model, on_point_selected: Callable | None = None):
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
        self._task = None

        self.view = None

    # -------------------------
    # binding
    # -------------------------
    def bind_view(self, view):
        self.view = view

    # -------------------------
    # controle da animação
    # -------------------------
    def start(self):
        """Inicia (ou reinicia) a animação."""
        self.progress = 0.0
        self._animation_done = False
        self._running = True

        self._ensure_loop()

    def stop(self):
        """Para a animação."""
        self._running = False
        self._animation_done = True

    def reset(self):
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
    def _ensure_loop(self):
        if not self.view:
            return

        page = getattr(self.view.control, "page", None)
        if not page:
            return

        # evita múltiplos loops concorrentes
        if self._task:
            return

        self._task = page.run_task(self._loop)

    async def _loop(self):
        try:
            while self._running and not self._animation_done:
                self.tick()
                await asyncio.sleep(0.016)  # ~60 FPS
        finally:
            self._task = None

    # -------------------------
    # lógica de animação
    # -------------------------
    def tick(self):
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

    def _update_active_index(self):
        total = len(self.model.points)

        if total <= 1:
            self.active_index = 0
            return

        self.active_index = int(self.progress * (total - 1))

    # -------------------------
    # seleção narrativa
    # -------------------------
    def select_point(self, point_id: str):
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
        if point_id == self.selected_point_id:
            return "selected"

        if point_id in self.clicked_point_ids:
            return "clicked"

        return "normal"

    def point_states(self) -> dict[int, str]:
        states = {}

        for index, point in enumerate(self.model.points):
            if point.id in self.clicked_point_ids:
                states[index] = "clicked"

            if point.id == self.selected_point_id:
                states[index] = "selected"

        return states

    # -------------------------
    # easing (opcional)
    # -------------------------
    def get_eased_progress(self):
        """
        Retorna progress com easing (ease-in-out).
        Não altera o estado interno.
        """
        return 0.5 - 0.5 * math.cos(self.progress * math.pi)
