from pathlib import Path

import flet as ft


def logos_row(logo1: Path, logo2: Path):

    return ft.Container(
        ft.Row(
            [
                ft.Image(src=str(logo1), height=120, fit=ft.BoxFit.CONTAIN),
                ft.Image(src=str(logo2), height=120, fit=ft.BoxFit.CONTAIN),
            ],
            alignment=ft.MainAxisAlignment.END,
            spacing=20,
        ),
        margin=ft.margin.only(top=20, bottom=10),
    )
