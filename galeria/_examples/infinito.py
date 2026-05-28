# galeria/_examples/infinito.py
"""Exemplo experimental de animação de símbolos de infinito em canvas."""

import asyncio
from typing import Any, override

import flet as ft
import flet.canvas as cv


@ft.control
class InfinityCanvas(ft.Stack):
    """Componente que desenha e anima símbolos de infinito."""

    def __init__(self, infinities_length: int, **kwargs: Any):
        """Configura quantidade de curvas e canvas interno."""
        super().__init__(**kwargs)
        self.infinities_length = infinities_length
        self.colors = ["#086A9A", "#D8523B", "#F8B023"]
        self.progress = 0.0
        self.animation_task = None

        # Cria o Canvas, que será o único filho do Stack
        self.canvas = cv.Canvas(
            shapes=[], expand=True, width=800, height=600, on_resize=self._on_canvas_resize
        )
        self.controls = [self.canvas]

    @override
    def did_mount(self):
        """Inicia a animação quando o controle é montado."""
        self.page.run_task(self._animate)
        self.update()

    @override
    def will_unmount(self):
        """Cancela a animação quando o controle é removido."""
        if self.animation_task:
            self.animation_task.cancel()

    def _on_canvas_resize(self, e: cv.CanvasResizeEvent):
        """Redesenha quando o Canvas é redimensionado."""
        self._draw_infinities(e.width, e.height, self.progress)

    def _draw_infinities(self, width: float, height: float, progress: float):
        """Desenha os símbolos de infinito com coordenadas normalizadas e sem clipping."""

        if width <= 0 or height <= 0:
            return

        shapes = []
        stroke_width = 10.0
        num_segments = 120

        # 🔒 Área segura (padding interno)
        pad_x = width * 0.1
        pad_y = height * 0.2

        safe_width = width - 2 * pad_x
        safe_height = height - 2 * pad_y

        def to_screen(nx, ny):
            """Converte coordenadas normalizadas (0-1) para pixels"""
            return (
                pad_x + nx * safe_width,
                pad_y + ny * safe_height,
            )

        # Centro único (fixo)
        center_x = 0.5
        center_y = 0.5

        for i in range(self.infinities_length):
            color = self.colors[i % len(self.colors)]

            # Offset progressivo (efeito "feixe")
            offset = (i - self.infinities_length / 2) * 0.015

            scale = 0.18 + (i * 0.01)

            cx = center_x + offset
            cy = center_y

            # Loop esquerdo
            c1 = self._generate_cubic_curve(
                start=to_screen(cx, cy),
                cp1=to_screen(cx - scale * 2, cy - scale * 2),
                cp2=to_screen(cx - scale * 2, cy + scale * 2),
                end=to_screen(cx, cy),
                num_segments=num_segments,
            )

            # Loop direito
            c2 = self._generate_cubic_curve(
                start=to_screen(cx, cy),
                cp1=to_screen(cx + scale * 2, cy - scale * 2),
                cp2=to_screen(cx + scale * 2, cy + scale * 2),
                end=to_screen(cx, cy),
                num_segments=num_segments,
            )

            all_points = c1 + c2[1:]

            # ✂️ Progresso da animação
            num_points_to_draw = max(2, int(len(all_points) * progress))

            elements = [cv.Path.MoveTo(*all_points[0])]

            for j in range(1, num_points_to_draw):
                elements.append(cv.Path.LineTo(*all_points[j]))

            path = cv.Path(
                elements=elements,
                paint=ft.Paint(
                    color=color,
                    stroke_width=stroke_width,
                    style=ft.PaintingStyle.STROKE,
                    stroke_cap=ft.StrokeCap.ROUND,
                    stroke_join=ft.StrokeJoin.ROUND,
                ),
            )

            shapes.append(path)

        self.canvas.shapes = shapes
        self.canvas.update()

    def _generate_cubic_curve(self, start, cp1, cp2, end, num_segments=100):
        """
        Gera uma lista de pontos (x, y) para uma curva cúbica de Bézier.
        """
        points = []
        for t in range(num_segments + 1):
            t_param = t / num_segments
            x = (
                (1 - t_param) ** 3 * start[0]
                + 3 * (1 - t_param) ** 2 * t_param * cp1[0]
                + 3 * (1 - t_param) * t_param**2 * cp2[0]
                + t_param**3 * end[0]
            )
            y = (
                (1 - t_param) ** 3 * start[1]
                + 3 * (1 - t_param) ** 2 * t_param * cp1[1]
                + 3 * (1 - t_param) * t_param**2 * cp2[1]
                + t_param**3 * end[1]
            )
            points.append((x, y))
        return points

    async def _animate(self):
        """Executa o loop contínuo de animação."""
        duration = 10.0
        steps = 180

        while True:
            for step in range(steps + 1):
                self.progress = step / steps

                if self.canvas.width and self.canvas.height:
                    self._draw_infinities(self.canvas.width, self.canvas.height, self.progress)

                await asyncio.sleep(duration / steps)

            self.progress = 0.0
            await asyncio.sleep(0.05)


def main(page: ft.Page) -> None:
    """Monta a página do exemplo de infinito animado."""
    page.title = "Símbolos de Infinito Animado"
    page.window_width = 1200
    page.window_height = 600
    infinity_canvas = InfinityCanvas(infinities_length=5, expand=True)
    page.add(ft.Container(content=infinity_canvas, expand=True))


ft.app(target=main)
