import flet as ft
import flet.canvas as cv


def main(page: ft.Page):
    page.title = "Timeline Fluida"
    page.bgcolor = "#F4F1EA"  # Cor de fundo similar à imagem
    page.padding = 50

    # Definição do caminho da linha (Curva de Bézier)
    paint = ft.Paint(
        color=ft.Colors.RED_800,
        stroke_width=5,
        style=ft.PaintingStyle.STROKE,
        stroke_cap=ft.StrokeCap.ROUND,
    )

    # Pontos da Timeline (X, Y, Texto, Ano)
    events = [
        (100, 300, "Início", "1967"),
        (400, 200, "Meio do mandato", "1968"),
        (700, 300, "Conclusão", "1969"),
    ]

    # Criando o desenho da curva
    canvas_shapes = [
        cv.Path(
            [
                cv.Path.MoveTo(50, 300),
                cv.Path.QuadraticTo(250, 450, 400, 250),  # Curva 1
                cv.Path.QuadraticTo(550, 50, 850, 300),  # Curva 2
            ],
            paint=paint,
        )
    ]

    # Adicionando os círculos e textos nos pontos específicos
    for x, y, desc, ano in events:  # type: ignore # noqa: B007
        # Círculo branco (ponto na linha)
        canvas_shapes.append(
            cv.Circle(x, y, 6, ft.Paint(color=ft.Colors.WHITE, style=ft.PaintingStyle.FILL))
        )
        canvas_shapes.append(cv.Circle(x, y, 6, paint))  # Borda vermelha

        # Textos informativos (posicionados acima ou abaixo do ponto)
        page.add(
            ft.Container(
                content=ft.Column(spacing=0),
                left=x - 20,
                top=y - 70 if y > 250 else y + 20,  # Alterna posição para não sobrepor
                # absolute_position=True,
            )
        )

    # Container principal para o Canvas
    chart = ft.Stack(
        [
            cv.Canvas(canvas_shapes, width=1000, height=500),
        ],
        width=1000,
        height=500,
    )

    page.add(
        ft.Text("Histórico Administrativo", size=32, weight="bold", color=ft.Colors.RED_900),
        ft.Divider(height=40, color="transparent"),
        chart,
    )


ft.app(target=main)
