from typing import Any

import flet as ft

from .models import Theme


def h1(theme: Theme, text: str, **kwargs: Any):
    return ft.Text(
        text,
        font_family=theme.typography.font_family,
        size=theme.typography.h1,
        weight=ft.FontWeight.BOLD,
        color=theme.text.primary,
        **kwargs,
    )


def h2(theme: Theme, text: str, **kwargs: Any):
    return ft.Text(
        text,
        font_family=theme.typography.font_family,
        size=theme.typography.h2,
        weight=ft.FontWeight.BOLD,
        color=theme.text.primary,
        **kwargs,
    )


def body(theme, text: str, **kwargs: Any):
    return ft.Text(
        text,
        font_family=theme.typography.font_family,
        size=theme.typography.body,
        color=theme.text.primary,
        **kwargs,
    )
