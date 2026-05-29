import os

import flet as ft

from galeria.main import main

if "PORT" in os.environ:
    os.environ["FLET_SERVER_PORT"] = os.environ["PORT"]


if __name__ == "__main__":
    ft.app(  # type: ignore
        target=main,
        assets_dir="galeria/assets",
    )
