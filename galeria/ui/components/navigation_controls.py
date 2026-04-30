from collections.abc import Callable

import flet as ft


class NavigationControls(ft.Row):
    def __init__(
        self,
        on_prev: Callable[[], None],
        on_next: Callable[[], None],
        alignment: ft.MainAxisAlignment = ft.MainAxisAlignment.END,
    ):
        def _build_button(icon, tooltip, handler):
            return ft.IconButton(
                icon=icon,
                tooltip=tooltip,
                on_click=lambda e: handler(),
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=8),
                    bgcolor={
                        ft.ControlState.HOVERED: ft.Colors.RED_200,
                        ft.ControlState.PRESSED: ft.Colors.RED_300,
                    },
                ),
            )

        super().__init__(
            alignment=alignment,
            controls=[
                _build_button(
                    ft.Icons.CHEVRON_LEFT,
                    "Anterior",
                    on_prev,
                ),
                _build_button(
                    ft.Icons.CHEVRON_RIGHT,
                    "Próximo",
                    on_next,
                ),
            ],
        )
