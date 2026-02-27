# navigation/navigator.py

import flet as ft


class Navigator:
    """
    Controller de navegação das páginas
    """

    def __init__(self, page: ft.Page):
        self.page = page

    def go(self, view: ft.Control):
        self.page.controls.clear()
        self.page.add(view)
        self.page.update()
