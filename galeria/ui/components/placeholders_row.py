import flet as ft


def placeholders_row(left_active: bool = False, right_active: bool = False):

    # Placeholders esquerdo e direito (decorativos, podem ser desligados)
    left_placeholder = ft.Container(
        width=80,
        height=80,
        bgcolor=ft.Colors.GREY_300 if left_active else None,
        visible=left_active,
        border_radius=10,
        content=ft.Text("L", color=ft.Colors.GREY_700) if left_active else None,
    )
    right_placeholder = ft.Container(
        width=80,
        height=80,
        bgcolor=ft.Colors.GREY_300 if right_active else None,
        visible=right_active,
        border_radius=10,
        content=ft.Text("R", color=ft.Colors.GREY_700) if right_active else None,
    )

    return ft.Container(
        content=ft.Row(
            [
                left_placeholder,
                ft.Container(expand=True),  # espaçador flexível
                right_placeholder,
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        margin=ft.margin.only(top=20),
    )
