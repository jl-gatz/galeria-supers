from collections.abc import Callable

import flet as ft


class NavigationControls(ft.Row):
    def __init__(
        self,
        on_prev: Callable[[], None],
        on_next: Callable[[], None],
        alignment: ft.MainAxisAlignment = ft.MainAxisAlignment.END,
    ):
        super().__init__(
            alignment=alignment,
            controls=[
                ft.IconButton(
                    icon=ft.Icons.CHEVRON_LEFT,
                    tooltip="Anterior",
                    on_click=lambda e: on_prev(),
                ),
                ft.IconButton(
                    icon=ft.Icons.CHEVRON_RIGHT,
                    tooltip="Próximo",
                    on_click=lambda e: on_next(),
                ),
            ],
        )
