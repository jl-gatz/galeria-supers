import flet as ft


def logos_row(logo1, logo2):

    return ft.Container(
        ft.Row(
            [
                ft.Image(src=logo1, height=120, fit=ft.BoxFit.CONTAIN),
                ft.Image(src=logo2, height=120, fit=ft.BoxFit.CONTAIN),
            ],
            alignment=ft.MainAxisAlignment.END,
            spacing=20,
        ),
        margin=ft.margin.only(top=20, bottom=10),
    )
