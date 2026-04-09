from pathlib import Path

import flet as ft


def logos_row(logo1: Path, logo2: Path):
    logo1 = Path(logo1)
    logo2 = Path(logo2)

    return ft.Container(
        ft.Row(
            [
                ft.Image(
                    src=str(logo1),
                    height=120,
                    fit=ft.BoxFit.CONTAIN,
                    data={
                        "type": "logo",
                        "nome": logo1.stem,
                    },
                ),
                ft.Image(
                    src=str(logo2),
                    height=120,
                    fit=ft.BoxFit.CONTAIN,
                    data={
                        "type": "logo",
                        "nome": logo2.stem,
                    },
                ),
            ],
            alignment=ft.MainAxisAlignment.END,
            spacing=20,
        ),
        margin=ft.Margin.only(top=20, bottom=10),
    )
