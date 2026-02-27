# Versão beta sem separar responsabilidade nenhuma...
import json
from pathlib import Path

import flet as ft

DATA_PATH = Path("data/supers.json")
ASSETS_PATH = Path("assets")


def carregar_supers():
    with open(DATA_PATH, encoding="utf-8") as f:
        return json.load(f)


def main(page: ft.Page):
    page.title = "Galeria dos Superintendentes"
    page.window.full_screen = True
    # page.window_maximized = True
    page.window.always_on_top = True

    # Remover barra de título e botões padrão
    page.window.title_bar_hidden = True
    page.window.title_bar_buttons_hidden = True
    page.window.frameless = True

    page.theme_mode = ft.ThemeMode.LIGHT
    page.scroll = ft.ScrollMode.AUTO
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    supers = carregar_supers()

    def abrir_super(super_data):
        page.controls.clear()

        slide_index = 0

        texto = ft.Text(
            super_data["historias"][slide_index],
            size=24,
            text_align=ft.TextAlign.CENTER,
            width=800,
        )

        def proximo(e):
            nonlocal slide_index
            if slide_index < len(super_data["historias"]) - 1:
                slide_index += 1
                texto.value = super_data["historias"][slide_index]
                page.update()

        def anterior(e):
            nonlocal slide_index
            if slide_index > 0:
                slide_index -= 1
                texto.value = super_data["historias"][slide_index]
                page.update()

        page.add(
            ft.Column(
                [
                    ft.Image(
                        src=str(ASSETS_PATH / super_data["foto"]),
                        width=300,
                        border_radius=20,
                    ),
                    ft.Text(
                        super_data["nome"],
                        size=32,
                        weight=ft.FontWeight.BOLD,
                    ),
                    texto,
                    ft.Row(
                        [
                            ft.Button("Anterior", on_click=anterior),
                            ft.Button("Próximo", on_click=proximo),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.TextButton("Voltar", on_click=lambda e: construir_home()),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
            )
        )
        page.update()

    def construir_home():
        page.controls.clear()

        cards = []

        for s in supers:
            card = ft.Container(
                content=ft.Column(
                    [
                        ft.Image(
                            src=str(ASSETS_PATH / s["foto"]),
                            width=200,
                            height=200,
                            fit="cover",
                            border_radius=ft.BorderRadius.all(100),
                        ),
                        ft.Text(
                            s["nome"],
                            size=20,
                            text_align=ft.TextAlign.CENTER,
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=20,
                on_click=lambda e, sup=s: abrir_super(sup),
            )
            cards.append(card)

        galeria = ft.Row(
            controls=cards,
            scroll=ft.ScrollMode.ALWAYS,
            alignment=ft.MainAxisAlignment.START,
            spacing=20,
        )

        # 🎯 Detector de fim de scroll
        async def on_scroll(e: ft.OnScrollEvent):
            # tolerância pequena para evitar ruído de float
            if e.pixels >= e.max_scroll_extent - 5:
                await galeria.scroll_to(offset=0, duration=8000)

        galeria.on_scroll = on_scroll

        page.add(
            ft.Column(
                [
                    ft.Text(
                        "Galeria dos Superintendentes",
                        size=36,
                        weight=ft.FontWeight.BOLD,
                    ),
                    galeria,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=40,
            )
        )
        page.update()

    construir_home()


# manter com ft.app (o formato mais novo não permite assets_dir?)
ft.app(target=main, assets_dir="assets")
