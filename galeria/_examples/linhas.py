# galeria/_examples/linhas.py
"""Exemplo experimental de linhas Bézier animadas em canvas."""

import asyncio
import math
from typing import Any

import flet as ft
import flet.canvas as cv


def main(page: ft.Page) -> None:
    """Monta a página com linhas animadas."""
    page.bgcolor = "#050505"
    num_linhas = 10
    canvas = cv.Canvas(width=600, height=400)

    page.add(ft.Container(content=canvas, alignment=ft.Alignment.CENTER, expand=True))

    async def animate() -> None:
        """Atualiza continuamente as curvas desenhadas no canvas."""
        t = 0
        while True:
            t += 0.05
            novas_formas: list[Any] = []
            for i in range(num_linhas):
                v1 = math.sin(t + i * 0.5) * 50
                v2 = math.cos(t + i * 0.5) * 50
                cor = ft.Colors.CYAN_400 if i % 2 == 0 else ft.Colors.AMBER_400
                linha = cv.Path(
                    elements=[
                        cv.Path.MoveTo(x=100, y=200),
                        cv.Path.CubicTo(
                            cp1x=250, cp1y=100 + v1, cp2x=450, cp2y=300 + v2, x=550, y=200
                        ),
                    ],
                    paint=ft.Paint(
                        color=ft.Colors.with_opacity(0.4, cor),
                        stroke_width=2,
                        style=ft.PaintingStyle.STROKE,
                        stroke_cap=ft.StrokeCap.ROUND,
                    ),
                )
                novas_formas.append(linha)
            canvas.shapes = novas_formas
            canvas.update()
            await asyncio.sleep(0.02)  # não bloqueia o loop

    page.run_task(animate)
    page.update()


run_app: Any = getattr(ft, "app")  # noqa: B009
run_app(target=main)


# def main2(page: ft.Page):
#     page.bgcolor = "#050505"
#     page.padding = 0

#     num_linhas = 15
#     canvas = cv.Canvas(expand=True)
#     page.add(ft.Container(canvas, alignment=ft.Alignment.CENTER, expand=True))

#     t = 0

#     def animar():
#         nonlocal t
#         t += 0.05
#         paths = []

#         off_x = math.sin(t * 0.5)
#         gradient_shader = ft.PaintLinearGradient(
#             begin=ft.alignment.Alignment(-1 + off_x, -1),
#             end=ft.alignment.Alignment(1 + off_x, 1),
#             colors=[ft.Colors.PURPLE_ACCENT, ft.Colors.CYAN_ACCENT, ft.Colors.PURPLE_ACCENT],
#         )

#         for i in range(num_linhas):
#             v1 = math.sin(t + i * 0.2) * 40
#             v2 = math.cos(t + i * 0.3) * 60

#             paths.append(
#                 cv.Path(
#                     elements=[
#                         cv.Path.MoveTo(100, 200),
#                         cv.Path.CubicTo(250, 50 + v1 + (i * 5), 450, 350 + v2 - (i * 5), 600, 200),
#                     ],
#                     paint=ft.Paint(
#                         stroke_width=1.5,
#                         style=ft.PaintingStyle.STROKE,
#                         gradient=gradient_shader,
#                         stroke_cap=ft.StrokeCap.ROUND,
#                     ),
#                 )
#             )

#         canvas.shapes = paths
#         canvas.update()

#     page.add_interval(20, animar)  # chama animar a cada 20ms
#     page.update()


# ft.app(target=main2)
