# galeria/ui/components/placeholders_row.py
"""Fábrica dos placeholders laterais opcionais da galeria."""

import flet as ft

from galeria.ui.theme.models import Theme


def placeholders_row(
    left_active: bool = False, right_active: bool = False, theme: Theme | None = None
) -> ft.Container:
    """Cria a linha de placeholders decorativos laterais."""
    bgcolor = (
        getattr(theme.base, "surface_variant", ft.Colors.GREY_300) if theme else ft.Colors.GREY_300
    )
    color = getattr(theme.text, "secondary", ft.Colors.GREY_700) if theme else ft.Colors.GREY_700
    radius = getattr(theme.radius, "sm", 10) if theme else 10
    margin_top = getattr(theme.spacing, "md", 20) if theme else 20

    # Placeholders esquerdo e direito (decorativos, podem ser desligados)
    left_placeholder = ft.Container(
        width=80,
        height=80,
        bgcolor=bgcolor if left_active else None,
        visible=left_active,
        border_radius=radius,
        content=ft.Text("L", color=color) if left_active else None,
    )
    right_placeholder = ft.Container(
        width=80,
        height=80,
        bgcolor=bgcolor if right_active else None,
        visible=right_active,
        border_radius=radius,
        content=ft.Text("R", color=color) if right_active else None,
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
        margin=ft.Margin.only(top=margin_top),
    )
