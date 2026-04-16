import flet as ft


class TimelineContainer(ft.Container):
    def __init__(self, view, **kwargs):
        super().__init__(**kwargs)
        self.view = view

    def did_mount(self):
        if hasattr(self.view.controller, "start"):
            self.view.controller.start()
