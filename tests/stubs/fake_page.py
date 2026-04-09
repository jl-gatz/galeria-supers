from tests.stubs.flet_harness_to_page import mount, unmount


class FakePage:
    def __init__(self):
        self.controls = []
        self.overlay_shown = None
        self.overlay_hidden = None
        self.history = []
        self.tasks = []
        self.scroll = None

    def add(self, *controls):
        self.controls.extend(controls)

    def remove(self, control):
        if control in self.controls:
            self.controls.remove(control)

    def update(self, *controls):
        pass

    def run_task(self, coro):
        import asyncio

        task = asyncio.create_task(coro)
        self.tasks.append(task)
        return task

    def show_overlay(self, component):
        self.overlay_shown = component
        mount(component, self)
        self.history.append(("show", component))

    def hide_overlay(self, component):
        self.overlay_hidden = component
        unmount(component)
        self.remove(component)
        self.history.append(("hide", component))
