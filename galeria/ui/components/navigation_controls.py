from collections.abc import Callable

import flet as ft

from galeria.ui.theme import RED_50, RED_55


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
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=8),
                        bgcolor={
                            ft.ControlState.HOVERED: RED_55,
                            ft.ControlState.PRESSED: RED_50,
                        },
                    ),
                ),
                ft.IconButton(
                    icon=ft.Icons.CHEVRON_RIGHT,
                    tooltip="Próximo",
                    on_click=lambda e: on_next(),
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=8),
                        bgcolor={
                            ft.ControlState.HOVERED: RED_55,
                            ft.ControlState.PRESSED: RED_50,
                        },
                    ),
                ),
            ],
        )
