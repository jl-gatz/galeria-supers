# galeria/ui/theme/styles.py
"""Estilos compostos para componentes que usam mais de um token."""

from dataclasses import dataclass

import flet as ft


@dataclass(frozen=True)
class PortraitCaptionStyle:
    """Tokens específicos da legenda sobre retratos."""

    name_size: int
    name_single_line_size: int
    subtitle_size: int
    name_weight: ft.FontWeight | str
    subtitle_weight: ft.FontWeight | str
    line_height: float
    spacing: int
    padding_horizontal: int
    padding_vertical: int
    compact_scale: float = 0.8
    compact_padding_scale: float = 0.75


@dataclass(frozen=True)
class ComponentStyles:
    """Agrupa estilos compostos usados por componentes da UI."""

    portrait_caption: PortraitCaptionStyle


def default_component_styles() -> ComponentStyles:
    """Cria o conjunto padrão de estilos compostos."""
    return ComponentStyles(
        portrait_caption=PortraitCaptionStyle(
            name_size=18,
            name_single_line_size=18,
            subtitle_size=16,
            name_weight=ft.FontWeight.BOLD,
            subtitle_weight=ft.FontWeight.W_500,
            line_height=1.05,
            spacing=4,
            padding_horizontal=16,
            padding_vertical=8,
        )
    )
