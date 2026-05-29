import asyncio
from collections.abc import Coroutine

from tests.stubs.flet_harness_to_page import mount, unmount


class FakePage:
    def __init__(self) -> None:
        self.controls: list[object] = []
        self.overlay_shown: object | None = None
        self.overlay_hidden: object | None = None
        self.history: list[tuple[str, object]] = []
        self.tasks: list[asyncio.Task[object]] = []
        self.scroll: object | None = None

    def add(self, *controls: object) -> None:
        self.controls.extend(controls)

    def remove(self, control: object) -> None:
        if control in self.controls:
            self.controls.remove(control)

    def update(self, *controls: object) -> None:
        pass

    def run_task(self, coro: Coroutine[object, object, object]) -> asyncio.Task[object]:
        task = asyncio.create_task(coro)
        self.tasks.append(task)
        return task

    def show_overlay(self, component: object) -> None:
        self.overlay_shown = component
        mount(component, self)
        self.history.append(("show", component))

    def hide_overlay(self, component: object) -> None:
        self.overlay_hidden = component
        unmount(component)
        self.remove(component)
        self.history.append(("hide", component))
