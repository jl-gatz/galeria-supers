# galeria/ui/components/timeline/view/timeline_container.py
"""Container que inicia a animação da timeline ao ser montado."""

from typing import Any, override

import flet as ft


class TimelineContainer(ft.Container):
    """Hospeda a timeline e aciona o controlador no lifecycle do Flet."""

    def __init__(self, view: Any, **kwargs: Any):
        super().__init__(**kwargs)
        self.view = view

    @override
    def did_mount(self) -> None:
        """Inicia a animação quando o container entra na página."""
        if hasattr(self.view.controller, "start"):
            self.view.controller.start()
