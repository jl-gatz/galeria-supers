from pathlib import Path
from typing import Any

import flet as ft

from galeria.ui.components.media import ThemedLogo


def logos_row(logo1: Path, logo2: Path, theme: Any | None = None):
    logo1 = Path(logo1)
    logo2 = Path(logo2)

    def _logo(path: Path):
        image_type = ThemedLogo if theme else ft.Image
        kwargs = {"theme": theme} if theme else {}

        return image_type(
            src=str(path),
            height=120,
            fit=ft.BoxFit.CONTAIN,
            data={
                "type": "logo",
                "nome": path.stem,
            },
            **kwargs,
        )

    return ft.Container(
        ft.Row(
            [
                _logo(logo1),
                _logo(logo2),
            ],
            alignment=ft.MainAxisAlignment.END,
            spacing=20,
        ),
        margin=ft.Margin.only(top=20, bottom=10),
    )
