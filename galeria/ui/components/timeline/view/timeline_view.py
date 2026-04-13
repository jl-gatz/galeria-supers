# galeria/ui/components/timeline/view/timeline_view.py

import base64

import flet as ft

EMPTY_SVG = """
<svg width="800" height="300" xmlns="http://www.w3.org/2000/svg"></svg>
"""

empty_base64 = base64.b64encode(EMPTY_SVG.encode()).decode()


class TimelineView:
    def __init__(self):
        self._image = ft.Image(src=empty_base64, width=800, height=300)
        self._root = ft.Container(
            content=self._image, width=800, height=300, bgcolor=ft.Colors.BLUE
        )

    def build(self):
        return self._root

    def update_path(self, path: str):
        svg = f'''<svg width="800" height="300" xmlns="http://www.w3.org/2000/svg">
            <rect width="100%" height="100%" fill="white"/>
            <path d="{path}" stroke="red" stroke-width="5" fill="none"/>
        </svg>'''
        # Codifica para base64 (mais seguro que URL-encode)
        b64 = base64.b64encode(svg.encode()).decode()
        self._image.src = f"data:image/svg+xml;base64,{b64}"
        self._image.update()
