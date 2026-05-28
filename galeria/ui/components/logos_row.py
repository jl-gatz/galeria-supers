# galeria/ui/components/logos_row.py
"""Fábrica da linha de logos institucionais da galeria."""

from pathlib import Path
from typing import Any

import flet as ft

from galeria.ui.components.media import ThemedLogo


def logos_row(logo1: Path, logo2: Path, theme: Any | None = None):
    """Cria a linha com dois logos, tematizados quando houver tema reativo."""
    logo1 = Path(logo1)
    logo2 = Path(logo2)

    def _logo(path: Path):
        """Cria um logo simples ou reativo conforme o tema recebido."""
        if theme:
            return ThemedLogo(
                theme_manager=theme,
                filename=path.name,
                height=120,
                fit=ft.BoxFit.CONTAIN,
                data={
                    "type": "logo",
                    "nome": path.stem,
                },
            )

        return ft.Image(
            src=str(path),
            height=120,
            fit=ft.BoxFit.CONTAIN,
            data={
                "type": "logo",
                "nome": path.stem,
            },
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
